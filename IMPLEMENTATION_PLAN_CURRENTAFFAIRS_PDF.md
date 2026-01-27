# Implementation Plan: Current Affairs MCQ/Descriptive from PDF

## Current System Understanding

### ProcessingLog Table Fields (Key)
```
- task_type: Determines what type of processing (pdf_to_mcq, currentaffairs_mcq_fetch, etc.)
- subject: For subject-based routing (polity, economics, etc.)
- pdf_upload: FK to PDFUpload
- start_page, end_page: Page range for PDF processing
- output_format: 'json', 'markdown', 'text'
- difficulty_level: Easy/Medium/Hard
- num_items: Number of items to generate
- log_details: JSON for storing additional metadata
```

### CurrentAffairsMCQ Model Fields (Critical)
```
ALWAYS REQUIRED:
- question, option_1, option_2, option_3, option_4, ans
- year_now, month, day (date fields - MUST map correctly)
- extra (stores explanation)

CATEGORY FIELDS (Boolean flags):
- Science_Techonlogy, National, International, Business_Economy_Banking
- Defence, Sports, Art_Culture, Awards_Honours, Persons_in_News
- Government_Schemes, appointment, rank, important_day, agreement, mythology, etc.
```

### CurrentAffairsDescriptive Model Fields (Critical)
```
ALWAYS REQUIRED:
- upper_heading, yellow_heading
- key_1, key_2, key_3, key_4
- all_key_points (TEXT field - contains /// separated points)
- year_now, month, day (date fields - MUST map correctly)
- paragraph (full text content)

CATEGORY FIELDS (Boolean flags):
- Science_Techonlogy, National, International, etc. (same as MCQ)
```

---

## Implementation Strategy

### STEP 1: Extend ProcessingForm in admin.py

Add new fields to ProcessPDFForm:
```python
class ProcessPDFForm(forms.Form):
    # ... existing fields ...
    
    # For Current Affairs Processing (optional)
    ca_type = forms.ChoiceField(
        label="Content Type",
        choices=[
            ('none', 'Subject-based (Polity, Economics, etc.)'),
            ('currentaffairs_mcq', 'Current Affairs MCQ'),
            ('currentaffairs_descriptive', 'Current Affairs Descriptive'),
        ],
        initial='none',
        required=False
    )
    
    # Date fields (for current affairs only)
    ca_date = forms.DateField(
        label="Date (leave blank for today)",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    ca_year = forms.ChoiceField(
        label="Year",
        choices=[('2025','2025'), ('2026','2026'), ('2027','2027'), ('2028','2028')],
        required=False
    )
    
    ca_auto_date = forms.BooleanField(
        label="Let LLM decide date and year",
        required=False
    )
```

### STEP 2: Update ProcessingLog Fields

Add to ProcessingLog model:
```python
# For Current Affairs Date Handling
ca_date = models.DateField(null=True, blank=True, help_text="Date for current affairs (if provided)")
ca_year = models.CharField(max_length=10, null=True, blank=True, help_text="Year for current affairs")
ca_auto_date = models.BooleanField(default=False, help_text="If True, LLM decides date/year from content")
```

### STEP 3: Modify process_pdf_with_options() View

Logic Flow:
```python
def process_pdf_with_options(request):
    if request.method == 'POST':
        form = ProcessPDFForm(request.POST)
        if form.is_valid():
            ca_type = form.cleaned_data.get('ca_type', 'none')
            
            if ca_type == 'none':
                # EXISTING: Subject-based (polity, economics, etc.)
                # Use chapter, difficulty, num_items logic
                task_type = 'pdf_to_mcq'  # or similar
                
            elif ca_type == 'currentaffairs_mcq':
                # NEW: Current Affairs MCQ from PDF
                task_type = 'pdf_currentaffairs_mcq'
                ca_date = form.cleaned_data.get('ca_date')
                ca_year = form.cleaned_data.get('ca_year')
                ca_auto_date = form.cleaned_data.get('ca_auto_date', False)
                
                log = ProcessingLog.objects.create(
                    task_type=task_type,
                    pdf_upload=pdf,
                    ca_date=ca_date if not ca_auto_date else None,
                    ca_year=ca_year if not ca_auto_date else None,
                    ca_auto_date=ca_auto_date,
                    # No chapter/difficulty needed
                )
                
            elif ca_type == 'currentaffairs_descriptive':
                # NEW: Current Affairs Descriptive from PDF
                task_type = 'pdf_currentaffairs_descriptive'
                # Same date handling as MCQ
                
            # Route based on task_type
            result = route_pdf_processing_task(log)
```

### STEP 4: Create CA-Specific Prompts in LLMPrompt Table

Create new prompts with source_url:
```
- 'pdf_to_currentaffairs_mcq_polity' → for CA MCQ from PDF
- 'pdf_to_currentaffairs_descriptive_polity' → for CA Descriptive from PDF
```

**Prompt for CA MCQ (already provided by user):**
```
You are an expert in creating multiple choice questions for competitive exams based on current affairs.
Based on the provided current affairs article, generate X high-quality MCQ questions.

Title: {title}
Content: {content}

CATEGORY CLASSIFICATION - IMPORTANT:
[Full category list...]

For each question, return in JSON format:
{
    "questions": [
        {
            "question": "...",
            "option_1": "...",
            "option_2": "...",
            "option_3": "...",
            "option_4": "...",
            "correct_answer": 1,
            "explanation": "...",
            "categories": ["National", "Art_Culture"]
        }
    ]
}
```

**Prompt for CA Descriptive:**
```
You are an expert in creating current affairs study material for competitive exams.
Based on the provided article, create study material.

Title: {title}
Content: {content}

For the content, provide:
1. upper_heading: A concise main heading (max 250 chars)
2. yellow_heading: A highlighted subheading for key point (max 250 chars)
3. key_1, key_2, key_3, key_4: Short key point titles
4. all_key_points: Comprehensive explanation using /// as separator for each point
5. categories: Array of relevant categories

Example format for all_key_points:
Heavy Water Board agreement for development of <b>deuterium labeled compounds...</b>///HWB currently operates 7 heavy water plants///During previous years, Indian industries imported...///Heavy Water is also known as <b>deuterium oxide (D2O).</b>

Return JSON:
{
    "upper_heading": "...",
    "yellow_heading": "...",
    "key_1": "...",
    "key_2": "...",
    "key_3": "...",
    "key_4": "...",
    "all_key_points": "...///...///...",
    "categories": ["National", "Business_Economy_Banking"]
}
```

### STEP 5: Create CA-Specific Processor in pdf_processor.py

Add methods:
```python
def process_currentaffairs_mcq(self, pdf_path, num_questions, content_type='mcq'):
    """Process PDF for Current Affairs MCQ"""
    # Extract content
    # Get CA MCQ prompt
    # Call LLM
    # Parse response
    # Return MCQ data with categories extracted
    
def process_currentaffairs_descriptive(self, pdf_path, content_type='descriptive'):
    """Process PDF for Current Affairs Descriptive"""
    # Extract content
    # Get CA Descriptive prompt
    # Call LLM
    # Parse response
    # Return descriptive data with all_key_points separated by ///
```

### STEP 6: Update task_router.py

Add logic to handle new task types:
```python
def route_pdf_processing_task(processing_log):
    task_type = processing_log.task_type
    
    if task_type == 'pdf_currentaffairs_mcq':
        processor = SubjectMCQGenerator()
        result = processor.process_currentaffairs_mcq(
            pdf_path=pdf_path,
            num_questions=processing_log.num_items or 5
        )
        # Save to currentaffairs_mcq table
        save_ca_mcq_to_database(result, processing_log)
        
    elif task_type == 'pdf_currentaffairs_descriptive':
        processor = SubjectMCQGenerator()
        result = processor.process_currentaffairs_descriptive(
            pdf_path=pdf_path
        )
        # Save to currentaffairs_descriptive table
        save_ca_descriptive_to_database(result, processing_log)
```

### STEP 7: Create Save Methods

```python
def save_ca_mcq_to_database(mcq_data, processing_log):
    """Save Current Affairs MCQ"""
    from bank.models import currentaffairs_mcq
    
    for question_data in mcq_data.get('questions', []):
        # Determine date/year
        if processing_log.ca_auto_date:
            # LLM provided date/year in response
            ca_date = question_data.get('date', timezone.now().date())
            ca_year = question_data.get('year')
        else:
            # Use provided date/year from form
            ca_date = processing_log.ca_date or timezone.now().date()
            ca_year = processing_log.ca_year
        
        # Extract categories
        categories = question_data.get('categories', [])
        
        ca_mcq = currentaffairs_mcq.objects.create(
            question=question_data.get('question'),
            option_1=question_data.get('option_1'),
            option_2=question_data.get('option_2'),
            option_3=question_data.get('option_3'),
            option_4=question_data.get('option_4'),
            ans=question_data.get('correct_answer', 1),
            extra=question_data.get('explanation'),
            day=ca_date,
            year_now=ca_year,
            # Set category flags based on categories array
            Science_Techonlogy='Science_Techonlogy' in categories,
            National='National' in categories,
            International='International' in categories,
            # ... all other categories ...
        )

def save_ca_descriptive_to_database(desc_data, processing_log):
    """Save Current Affairs Descriptive"""
    from bank.models import currentaffairs_descriptive
    
    # Determine date/year (same logic as MCQ)
    ca_date = processing_log.ca_date or timezone.now().date()
    ca_year = processing_log.ca_year
    
    # Extract categories
    categories = desc_data.get('categories', [])
    
    ca_desc = currentaffairs_descriptive.objects.create(
        upper_heading=desc_data.get('upper_heading'),
        yellow_heading=desc_data.get('yellow_heading'),
        key_1=desc_data.get('key_1'),
        key_2=desc_data.get('key_2'),
        key_3=desc_data.get('key_3'),
        key_4=desc_data.get('key_4', ''),
        all_key_points=desc_data.get('all_key_points'),  # Contains /// separator
        paragraph=desc_data.get('content'),
        day=ca_date,
        year_now=ca_year,
        # Set category flags
        Science_Techonlogy='Science_Techonlogy' in categories,
        National='National' in categories,
        # ... all other categories ...
    )
```

---

## Database Changes Needed

### ProcessingLog Model (add fields)
```python
ca_date = models.DateField(null=True, blank=True)
ca_year = models.CharField(max_length=10, null=True, blank=True)
ca_auto_date = models.BooleanField(default=False)
```

### Add Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Testing Workflow

1. **Upload PDF** with current affairs content
2. **Select** "Current Affairs MCQ" or "Current Affairs Descriptive"
3. **Choose date handling**:
   - Leave blank + unchecked → uses today's date + current year
   - Enter date/year + unchecked → uses provided date/year for all MCQs
   - Checked → LLM decides from content
4. **Submit** → ProcessingLog created
5. **Route** → Processor detects task_type → Calls appropriate processor
6. **Save** → Results saved to currentaffairs_mcq or currentaffairs_descriptive with categories

---

## Key Implementation Notes

✅ **Category Mapping**: Response categories array → Boolean flags on model
✅ **Date Handling**: Three modes (today, provided, LLM-decides)
✅ **All Key Points**: Preserve /// separators in all_key_points field
✅ **Prompt Template**: Use /// for all_key_points in prompt example
✅ **LLM Provider**: Increased token limit (8192) ensures complete responses
✅ **Field Naming**: 'extra' for explanation (not 'explanation')

