# Prompt Routing - Complete Mapping for All 4 Cases

## Overview
The system uses **task_type** and **subject** parameters to determine which LLM prompt to use. The routing function `get_llm_prompt_for_task()` is in `/genai/tasks/task_router.py` lines 56-105.

---

## The Routing Logic

```python
def get_llm_prompt_for_task(task_type: str, subject: str, prompt_type: str = 'mcq'):
    if task_type.startswith('pdf_to_'):
        # Case 1: pdf_to_mcq_polity, pdf_to_descriptive_computer, etc.
        source_url = f"{task_type}_{subject}"
    else:
        # Case 2: pdf_currentaffairs_mcq, pdf_currentaffairs_descriptive
        source_url = f"pdf_{subject}_{prompt_type}"
    
    # Search for specific prompt, fallback to default (empty source_url)
```

---

## The 4 Use Cases

### **CASE 1: PDF → Subject MCQ** ✅
**Where:** Admin form → PDF upload → Subject MCQ processing

**Admin Code:** `/genai/admin.py` line 870
```python
task_type='pdf_to_mcq',
subject=form.cleaned_data['subject']  # e.g., 'polity', 'biology'
```

**Routing Logic:**
- `task_type = 'pdf_to_mcq'` (starts with 'pdf_to_')
- `subject = 'polity'` (or 'biology', 'economics', etc.)
- `prompt_type = 'mcq'` (default)
- **Search source_url:** `pdf_to_mcq_polity`
- **Fallback:** `source_url=''` + `prompt_type='mcq'` (default prompt)

**Prompt Creation Needed?** 
- ⚠️ Check if `pdf_to_mcq_polity` exists
- If NOT: Falls back to default 'mcq' prompt (should exist)

**Example Processing:**
```
Input: polity.pdf
↓
Task: task_type='pdf_to_mcq', subject='polity'
↓
Searches: Prompt with source_url='pdf_to_mcq_polity'
↓
If found: Use that specific prompt
If not found: Use default prompt (source_url='')
↓
Output: MCQs saved to polity table
```

---

### **CASE 2: PDF → Subject Descriptive** ⚠️
**Where:** Admin form → PDF upload → Subject Descriptive processing

**Admin Code:** `/genai/admin.py` (same section, different processing_type)

**Routing Logic:**
- `task_type = 'pdf_to_descriptive'` (starts with 'pdf_to_')
- `subject = 'polity'` (or 'biology', 'economics', etc.)
- `prompt_type = 'descriptive'`
- **Search source_url:** `pdf_to_descriptive_polity`
- **Fallback:** `source_url=''` + `prompt_type='descriptive'` (default prompt)

**Prompt Creation Needed?**
- ⚠️ Check if `pdf_to_descriptive_polity` exists
- If NOT: Falls back to default 'descriptive' prompt (should exist)

---

### **CASE 3: PDF → Current Affairs MCQ** ✅ IMPLEMENTED
**Where:** Admin form → PDF upload → Current Affairs MCQ

**Admin Code:** `/genai/admin.py` line 932
```python
task_type='pdf_currentaffairs_mcq',
```

**Routing Logic:**
- `task_type = 'pdf_currentaffairs_mcq'` (does NOT start with 'pdf_to_')
- `subject = 'current_affairs'` (hardcoded)
- `prompt_type = 'mcq'` (default)
- **Search source_url:** `pdf_current_affairs_mcq`
- **Fallback:** `source_url=''` + `prompt_type='mcq'` (default prompt)

**Prompt Created:** ✅ YES
- **ID:** 49
- **source_url:** `pdf_current_affairs_mcq`
- **prompt_type:** `mcq`
- **Status:** Active

**Why This Routing Works:**
```
Input: currentaffairs.pdf
↓
Task: task_type='pdf_currentaffairs_mcq', subject='current_affairs'
↓
Logic: NOT starts with 'pdf_to_' → source_url = f"pdf_{subject}_{prompt_type}"
       = f"pdf_current_affairs_mcq"
↓
Searches: Prompt with source_url='pdf_current_affairs_mcq'
↓
Found: ✅ Uses the comprehensive CA MCQ prompt (ID 49)
↓
Output: MCQs saved to currentaffairs_mcq table with:
  - Options (A/B/C/D)
  - Category (Politics, Economy, International, etc.)
  - Year & Date
```

---

### **CASE 4: PDF → Current Affairs Descriptive** ⚠️
**Where:** Admin form → PDF upload → Current Affairs Descriptive

**Admin Code:** `/genai/admin.py` line 988
```python
task_type='pdf_currentaffairs_descriptive',
```

**Routing Logic:**
- `task_type = 'pdf_currentaffairs_descriptive'` (does NOT start with 'pdf_to_')
- `subject = 'current_affairs'` (hardcoded)
- `prompt_type = 'descriptive'`
- **Search source_url:** `pdf_current_affairs_descriptive`
- **Fallback:** `source_url=''` + `prompt_type='descriptive'` (default prompt)

**Prompt Needed?**
- ⚠️ Check if `pdf_current_affairs_descriptive` exists
- If NOT: Falls back to default 'descriptive' prompt (should exist)

---

## Prompt Summary Table

| Case | task_type | subject | prompt_type | Searches for source_url | Status | ID |
|------|-----------|---------|-------------|-------------------------|--------|-----|
| **1** | pdf_to_mcq | polity | mcq | `pdf_to_mcq_polity` | ⚠️ ? | ? |
| **2** | pdf_to_descriptive | polity | descriptive | `pdf_to_descriptive_polity` | ⚠️ ? | ? |
| **3** | pdf_currentaffairs_mcq | current_affairs | mcq | `pdf_current_affairs_mcq` | ✅ YES | 49 |
| **4** | pdf_currentaffairs_descriptive | current_affairs | descriptive | `pdf_current_affairs_descriptive` | ⚠️ ? | ? |

---

## Key Points

### ✅ What's Working
1. **PDF → Current Affairs MCQ** (Case 3)
   - Prompt created with ID 49
   - source_url = `pdf_current_affairs_mcq`
   - Includes category classification in the prompt
   - System successfully extracts and saves MCQs with categories

2. **Fallback Mechanism**
   - If specific prompt not found, system falls back to default prompt
   - Default prompts use empty `source_url=''`
   - Default MCQ and descriptive prompts should exist

### ⚠️ What Needs Checking
1. **Subject-specific prompts** (Cases 1 & 2)
   - Do `pdf_to_mcq_polity` type prompts exist?
   - If not, system falls back to default (which is OK)
   
2. **Current Affairs Descriptive** (Case 4)
   - Do we need a specific prompt or use default?
   - If using specific: Need to create `pdf_current_affairs_descriptive`

### 📋 Required Prompts (Minimum)

**MUST EXIST (Fallback defaults):**
- `source_url=''`, `prompt_type='mcq'` - Default MCQ prompt
- `source_url=''`, `prompt_type='descriptive'` - Default descriptive prompt

**OPTIONAL (Specific overrides):**
- `pdf_to_mcq_polity` - Override default for polity MCQ
- `pdf_to_mcq_biology` - Override default for biology MCQ
- `pdf_to_descriptive_polity` - Override default for polity descriptive
- `pdf_current_affairs_descriptive` - Override default for CA descriptive

---

## Implementation Timeline

### Phase 1: Subject MCQ (Case 1)
- ✅ Form submission captures processing_type='subject_mcq'
- ✅ Sets task_type='pdf_to_mcq', subject='polity'
- ⚠️ Prompt search: `pdf_to_mcq_polity` → Falls back to default

### Phase 2: PDF → Current Affairs MCQ (Case 3)
- ✅ Form submission captures processing_type='ca_mcq'
- ✅ Sets task_type='pdf_currentaffairs_mcq'
- ✅ Prompt search: `pdf_current_affairs_mcq` → **FOUND (ID 49)**
- ✅ Questions generated with categories
- ✅ Data saved to currentaffairs_mcq table

### Phase 3: Current Affairs Descriptive (Case 4)
- ✅ Form submission captures processing_type='ca_descriptive'
- ✅ Sets task_type='pdf_currentaffairs_descriptive'
- ⚠️ Prompt search: `pdf_current_affairs_descriptive` → Falls back to default

### Phase 4: Subject Descriptive (Case 2)
- ⚠️ Not yet tested
- ⚠️ Prompt search: `pdf_to_descriptive_polity` → Falls back to default

---

## Testing Command

To verify which prompts exist, run:

```bash
cd django_project
python manage.py shell

from genai.models import LLMPrompt
# Show all prompts
for p in LLMPrompt.objects.filter(is_active=True):
    print(f"ID: {p.id:3} | source_url: {p.source_url:40} | prompt_type: {p.prompt_type:15}")
```

---

## Answer to "how it is working for both the cases"

**The Prompt Routing Works as follows:**

1. **Different task_types trigger different routing:**
   - `pdf_to_*` → Builds source_url as `{task_type}_{subject}`
   - `pdf_currentaffairs_*` → Builds source_url as `pdf_{subject}_{prompt_type}`

2. **Searches for specific prompt first:**
   - Current Affairs MCQ: Searches `pdf_current_affairs_mcq` → ✅ FOUND (ID 49)
   - Subject MCQ: Searches `pdf_to_mcq_polity` → Uses default if not found

3. **Falls back to default if not found:**
   - Every task_type can use a default prompt (source_url='')
   - Default prompts should be more generic/general

4. **Why Current Affairs MCQ works but others might not:**
   - We explicitly created the `pdf_current_affairs_mcq` prompt
   - It's specific with category extraction logic
   - Other cases rely on default prompts (which must exist)

---

## Prompt Name I Used for Case 3

**Prompt ID:** 49
**source_url:** `pdf_current_affairs_mcq`
**prompt_type:** `mcq`

**Key Feature:** Includes category classification
```
Categories to classify:
- Politics (domestic/international political events)
- Economy (economic indicators, GDP, inflation)
- International Relations (trade, diplomacy)
- Others (miscellaneous current affairs)
```

This routing ensures that when you process a Current Affairs PDF, the system specifically uses the comprehensive CA MCQ prompt (ID 49) that knows how to extract and classify current affairs MCQs with proper categories.
