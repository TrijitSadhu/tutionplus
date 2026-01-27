# PDF/Document Processing System - Design & Implementation Plan

## Current Status Analysis

### Existing Infrastructure ✅
1. **ProcessingLog Model** - Generic task tracking with:
   - User authentication (`created_by = ForeignKey(User)`)
   - Task type selection
   - Status tracking (pending, running, completed, failed)
   - PDF support (`pdf_upload = ForeignKey(PDFUpload)`)
   - Progress tracking

2. **PDFUpload Model** - PDF file management with:
   - User tracking (`uploaded_by`)
   - Subject classification
   - Status monitoring
   - Text extraction capability

3. **LLMPrompt Model** - Dynamic prompts:
   - Multiple prompts per type/source
   - Default prompt fallback
   - Database-driven (reusable)

4. **Admin Interface** - Full CRUD + Actions:
   - Custom admin panels
   - Action buttons
   - Status badges
   - Task triggering

## Proposed Enhancement: Subject-Wise PDF Processing

### New Task Types Needed
```
TASK_TYPES = [
    # Current (already exist)
    ('currentaffairs_mcq_fetch', 'Current Affairs MCQ Fetch from URL'),
    ('currentaffairs_descriptive_fetch', 'Current Affairs Descriptive Fetch from URL'),
    
    # NEW: PDF-based processing
    ('pdf_to_mcq', 'PDF → MCQ Questions'),
    ('pdf_to_descriptive', 'PDF → Descriptive Answers'),
    ('pdf_to_polity', 'PDF → Polity Notes'),
    ('pdf_to_economics', 'PDF → Economics Notes'),
    ('pdf_to_math', 'PDF → Math Problems'),
    ('pdf_to_physics', 'PDF → Physics Notes'),
    ('pdf_to_history', 'PDF → History Notes'),
    ('pdf_to_geography', 'PDF → Geography Notes'),
]
```

### Processing Subject Matter
- **MCQ** - Multiple choice questions with 4 options and answers
- **Descriptive** - Long-form answers/explanations
- **Subject Notes** - Topic-wise summaries (Polity, Economics, History, Geography, etc.)
- **Math** - Mathematical problems with solutions
- **Physics/Chemistry** - Problem solutions, formulas

### Enhancement to ProcessingLog

#### Option 1: Extend Existing ProcessingLog (RECOMMENDED)
Add fields for subject-specific tasks:
```python
# Subject & Task Configuration
subject = models.CharField(
    max_length=50,
    choices=[('polity', 'Polity'), ('economics', 'Economics'), ...],
    null=True, blank=True,
    help_text="Subject for PDF processing"
)

# Output configuration
output_format = models.CharField(
    max_length=50,
    choices=[('json', 'JSON'), ('markdown', 'Markdown'), ('text', 'Plain Text')],
    default='json'
)

# Pages to process (optional - process specific pages)
start_page = models.IntegerField(null=True, blank=True)
end_page = models.IntegerField(null=True, blank=True)

# Difficulty level (for MCQ/Math)
difficulty_level = models.CharField(
    max_length=20,
    choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
    null=True, blank=True
)

# Number of items to generate
num_items = models.IntegerField(default=10, help_text="Number of questions/items to generate")
```

### Database Structure Decision

**Using SINGLE table (ProcessingLog) with multiple task types:**
- ✅ Simpler schema
- ✅ Centralized tracking
- ✅ Reuses authentication (created_by)
- ✅ Consistent progress tracking
- ✅ Subject fields are optional (null=True)
- ✅ Extensible for future task types

**Alternative: Separate tables**
- Would need duplicate auth fields
- More complex queries
- Not recommended

## Implementation Roadmap

### Phase 1: Model Enhancement
- [ ] Add subject field to ProcessingLog
- [ ] Add output_format field
- [ ] Add page_range fields (start_page, end_page)
- [ ] Add difficulty_level field
- [ ] Add num_items field
- [ ] Create migration

### Phase 2: Admin Interface Update
- [ ] Create ProcessingLogAdmin (extend existing)
- [ ] Add conditional field display based on task_type
- [ ] Add task triggering actions
- [ ] Add progress monitoring
- [ ] Display PDF name linked to ProcessingLog

### Phase 3: LLM Prompt Management
- [ ] Create subject-specific prompts
- [ ] Add prompt templates for each task type:
  - pdf_to_mcq
  - pdf_to_descriptive
  - pdf_to_polity
  - pdf_to_economics
  - pdf_to_math
  - etc.

### Phase 4: Processing Logic
- [ ] Extract text from PDF using PyPDF2/pdfplumber
- [ ] Split content by pages/chapters
- [ ] Send to appropriate LLM with subject-specific prompt
- [ ] Parse LLM response
- [ ] Save output to database/storage

### Phase 5: Output Storage
- [ ] Create GeneratedContent model (optional):
  - Stores generated MCQs/Descriptive answers
  - Links to ProcessingLog
  - Subject-wise categorization
  - Retrievable by users

## Example Workflow

### User Workflow:
```
1. Admin Portal → Upload PDF
   ↓
2. PDF appears in PDFUpload list
   ↓
3. Create ProcessingLog entry:
   - Select PDF file
   - Select task_type: 'pdf_to_mcq'
   - Select subject (auto-filled from PDF if possible)
   - Set num_items: 10
   - Set difficulty_level: 'medium'
   ↓
4. Click "Process" button (action)
   ↓
5. Backend processes:
   - Extract text from PDF pages
   - Send to LLM with mcq-specific prompt
   - Save 10 MCQs to database
   - Update ProcessingLog status: 'completed'
   ↓
6. Results viewable:
   - In ProcessingLog progress tracking
   - In separate GeneratedContent records
   - Export as JSON/CSV
```

## File Structure for Generated Content

Each task can output:
- **MCQ**: `[{question, option_a, option_b, option_c, option_d, answer, explanation}, ...]`
- **Descriptive**: `[{topic, answer, source_page}, ...]`
- **Notes**: `{chapter: {key_points: [], summary: ""}}`

## Database Migrations Required

```python
# Add to ProcessingLog
subject = models.CharField(max_length=50, null=True, blank=True)
output_format = models.CharField(max_length=50, default='json')
start_page = models.IntegerField(null=True, blank=True)
end_page = models.IntegerField(null=True, blank=True)
difficulty_level = models.CharField(max_length=20, null=True, blank=True)
num_items = models.IntegerField(default=10)
```

## Questions to Answer

1. Should generated content be stored separately or embedded in log?
   → Separate GeneratedContent table recommended for:
   - Easy retrieval by users
   - Bulk export capability
   - Reusability across tests
   - Linking to other entities (tests, courses)

2. Should we support batch processing (multiple PDFs)?
   → Yes, ProcessingLog already supports:
   - Progress tracking (total_items, processed_items)
   - Multiple PDFs can reference same task type

3. How to handle multi-page PDFs?
   → Options:
   - Process all at once
   - Process page ranges (start_page, end_page)
   - Process by chapter if available
   - User-selected approach in UI

## Recommendations

✅ **Use existing ProcessingLog table** with new fields
✅ **Leverage existing User authentication** 
✅ **Create subject-specific LLM prompts** in database
✅ **Reuse admin interface patterns** already established
✅ **Add GeneratedContent table** for output storage
✅ **Support page-range processing** for large PDFs

This approach:
- Minimizes database overhead
- Reuses proven patterns
- Maintains consistency
- Scales easily for new task types
- Leverages existing auth system
