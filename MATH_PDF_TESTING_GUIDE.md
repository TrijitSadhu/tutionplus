# Math PDF Processing - Testing Guide

## Quick Start Testing

### Prerequisites

1. **Install OCR Dependencies**:
```powershell
pip install paddleocr easyocr pytesseract pdf2image PyPDF2 pillow numpy
```

2. **System Dependencies**:
- Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
- Install Poppler for pdf2image: https://github.com/oschwartz10612/poppler-windows/releases

### Test Scenario 1: Single Page PDF Processing

**Objective**: Test basic PDF upload and single page processing with LLM classification

**Steps**:
1. Navigate to admin: `/admin/genai/mathproblemgeneration/`
2. Click "Add Math Problem Generation"
3. **DO NOT** enter expression (leave blank)
4. Upload a math PDF file (e.g., algebra problems)
5. Leave chapter and difficulty blank (let LLM decide)
6. Click "Save"
7. Find your new entry in the list
8. **Click the GO button** in the Action column
9. On the configuration form:
   - ✅ Check "Let LLM decide chapter"
   - ✅ Check "Let LLM decide difficulty level"
   - ✅ Check "Use PaddleOCR"
   - ✅ Check "Process PDF file"
   - Set "Page From": 0
   - Set "Page To": 0 (single page)
   - ✅ Check "Process all MCQs in page range"
10. Click "Proceed"

**Expected Results**:
- Success message: "PDF processing started successfully"
- Redirect to admin list
- Check `bank.math` table for new MCQs
- Check `ProcessingLog` for detailed log entry

**Verify**:
```sql
-- Check saved MCQs
SELECT chapter, difficulty, question, source 
FROM bank_math 
WHERE source = 'genai-pdf' 
ORDER BY id DESC 
LIMIT 5;

-- Check processing log
SELECT task_type, status, result_summary 
FROM genai_processinglog 
ORDER BY started_at DESC 
LIMIT 1;
```

### Test Scenario 2: Page Range Processing

**Objective**: Test processing a specific page range

**Steps**:
1. Use existing PDF entry or create new one
2. Click GO button
3. Configure:
   - ✅ Check "Use PaddleOCR"
   - ✅ Check "Use EasyOCR" (fallback)
   - ✅ Check "Process PDF file"
   - Set "Page From": 5
   - Set "Page To": 10
   - ✅ Check "Process all MCQs in page range"
4. Click "Proceed"

**Expected Results**:
- Pages 5-10 processed (6 pages total)
- Multiple MCQs extracted from each page
- All MCQs saved to bank.math

### Test Scenario 3: Full PDF with Chunks

**Objective**: Test chunked processing of entire PDF

**Steps**:
1. Use existing PDF entry or create new one
2. Click GO button
3. Configure:
   - ✅ Check "Let LLM decide chapter"
   - ✅ Check "Use PaddleOCR"
   - ✅ Check "Use EasyOCR"
   - ✅ Check "Use Tesseract" (all engines)
   - ✅ Check "Process PDF file"
   - Set "Page From": 0
   - Set "Page To": 0 (entire PDF)
   - ✅ Check "Process entire PDF in chunks"
   - Set chunks: 5 pages at a time
4. Click "Proceed"

**Expected Results**:
- Entire PDF processed in 5-page chunks
- MCQs from all pages saved
- Processing log shows chunk progress

### Test Scenario 4: Expression Mode (Regression)

**Objective**: Verify existing expression mode still works

**Steps**:
1. Create new MathProblemGeneration
2. Enter expression: `x^2 + 5x + 6 = 0`
3. Set difficulty: medium
4. **DO NOT** upload PDF
5. Click "Save"
6. Select entry in admin list
7. Use "Convert to LaTeX" action
8. Use "Generate Math MCQs" action

**Expected Results**:
- LaTeX output generated correctly
- MCQs generated from expression
- All saved to MathProblemGeneration model (not bank.math)
- Existing workflow unchanged

### Test Scenario 5: OCR Fallback

**Objective**: Test OCR engine fallback mechanism

**Steps**:
1. Upload a complex PDF (with images, diagrams)
2. Click GO button
3. Configure:
   - ✅ Check "Use PaddleOCR"
   - ✅ Check "Use EasyOCR"
   - ✅ Check "Use Tesseract"
   - Process single page with complex content
4. Monitor logs during processing

**Expected Results**:
- If PaddleOCR fails → tries EasyOCR
- If EasyOCR fails → tries Tesseract
- First successful extraction used
- Detailed logging shows fallback chain

### Test Scenario 6: Manual Classification

**Objective**: Test manual chapter/difficulty without LLM

**Steps**:
1. Upload PDF
2. Set chapter: "Algebra"
3. Set difficulty: "medium"
4. Click GO button
5. Configure:
   - ✅ **UNCHECK** "Let LLM decide chapter"
   - ✅ **UNCHECK** "Let LLM decide difficulty"
   - ✅ Check "Use PaddleOCR"
   - Process page range
6. Click "Proceed"

**Expected Results**:
- Uses provided chapter and difficulty
- No LLM classification calls
- Faster processing
- MCQs saved with manual values

## Error Testing

### Error Test 1: No OCR Engine Selected

**Steps**:
1. Click GO button
2. **Uncheck all OCR engines**
3. Check "Process PDF file"
4. Click "Proceed"

**Expected Result**:
- Form validation error: "Please select at least one OCR engine"

### Error Test 2: Invalid Page Range

**Steps**:
1. Click GO button
2. Set "Page From": 10
3. Set "Page To": 5 (less than from)
4. Click "Proceed"

**Expected Result**:
- Form validation error: "Page From cannot be greater than Page To"

### Error Test 3: PDF Without Expression

**Steps**:
1. Create entry with NO expression and NO PDF
2. Click GO button
3. Try to process

**Expected Result**:
- Error message: "No PDF file or expression to process"

### Error Test 4: OCR Failure on All Engines

**Steps**:
1. Upload a corrupted PDF or image-only PDF
2. Process with all OCR engines
3. Monitor logs

**Expected Result**:
- All OCR engines fail gracefully
- Error logged: "All OCR engines failed"
- ProcessingLog updated with failure status
- No crash or exception

## Performance Testing

### Performance Test 1: Large PDF (100+ pages)

**Test**: Process 100-page PDF in chunks

**Configuration**:
- Chunks: 10 pages at a time
- All OCR engines enabled
- LLM classification enabled

**Metrics to Track**:
- Total processing time
- Time per page
- Time per chunk
- OCR fallback frequency
- Memory usage

**Expected**:
- ~10 seconds per page (varies by OCR and content)
- Consistent memory usage (no leaks)
- Progress logged for each chunk

### Performance Test 2: Concurrent Processing

**Test**: Multiple users processing PDFs simultaneously

**Steps**:
1. Create 5 different PDF entries
2. Have 5 users click GO simultaneously
3. Monitor system performance

**Metrics**:
- Response time degradation
- Database connection pool
- Memory usage
- CPU usage

**Expected**:
- Graceful handling of concurrent requests
- No deadlocks or race conditions
- Queue processing if needed

## Verification Queries

### Check Recent Processing Logs
```sql
SELECT 
    id,
    task_type,
    status,
    parameters->>'problem_id' as problem_id,
    parameters->>'config' as config,
    result_summary->>'total_pages' as pages,
    result_summary->>'mcqs_extracted' as mcqs,
    started_at,
    completed_at,
    EXTRACT(EPOCH FROM (completed_at - started_at)) as duration_seconds
FROM genai_processinglog
WHERE task_type = 'math_pdf_processing'
ORDER BY started_at DESC
LIMIT 10;
```

### Check Saved MCQs
```sql
SELECT 
    chapter,
    difficulty,
    LEFT(question, 50) as question_preview,
    source,
    created_at
FROM bank_math
WHERE source = 'genai-pdf'
ORDER BY id DESC
LIMIT 20;
```

### Check Problem Status
```sql
SELECT 
    id,
    chapter,
    difficulty,
    status,
    pdf_file IS NOT NULL as has_pdf,
    latex_output IS NOT NULL as has_latex,
    generated_mcqs IS NOT NULL as has_mcqs,
    error_message,
    created_at,
    processed_at
FROM genai_mathproblemgeneration
ORDER BY created_at DESC
LIMIT 10;
```

### Count MCQs by Chapter
```sql
SELECT 
    chapter,
    difficulty,
    COUNT(*) as mcq_count,
    MIN(created_at) as first_created,
    MAX(created_at) as last_created
FROM bank_math
WHERE source = 'genai-pdf'
GROUP BY chapter, difficulty
ORDER BY chapter, difficulty;
```

## Debug Tips

### Enable Detailed Logging

Add to Django settings:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'genai.tasks.math_processor': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### Check OCR Engine Status

Run in Django shell:
```python
from genai.tasks.math_processor import OCRDispatcher

# Test OCR engines
dispatcher = OCRDispatcher(use_paddle=True, use_easy=True, use_tesseract=True)
result = dispatcher.extract_text('path/to/test.pdf', page_number=0)
print(f"Extracted text length: {len(result) if result else 0}")
```

### Test LLM Classification

Run in Django shell:
```python
from genai.tasks.math_processor import MathPDFProcessor

processor = MathPDFProcessor()

# Test chapter classification
test_content = "Solve the quadratic equation: x^2 + 5x + 6 = 0"
chapter_result = processor.classify_chapter_by_llm(test_content)
print(f"Chapter: {chapter_result}")

# Test difficulty classification
difficulty_result = processor.classify_difficulty_by_llm(test_content)
print(f"Difficulty: {difficulty_result}")
```

### Test MCQ Extraction

Run in Django shell:
```python
from genai.tasks.math_processor import MathPDFProcessor

processor = MathPDFProcessor()

test_text = """
1. What is 2 + 2?
A) 2
B) 3
C) 4
D) 5

2. Solve: x + 5 = 10
A) x = 3
B) x = 5
C) x = 10
D) x = 15
"""

mcqs = processor._extract_mcqs_from_text(test_text, 'Algebra', 'easy')
print(f"Extracted {len(mcqs)} MCQs")
for i, mcq in enumerate(mcqs, 1):
    print(f"\nMCQ {i}:")
    print(f"  Question: {mcq['question'][:50]}...")
    print(f"  Answer: {mcq['correct_answer']}")
```

## Common Issues & Solutions

### Issue 1: OCR Installation Errors

**Error**: `ImportError: No module named 'paddleocr'`

**Solution**:
```powershell
pip install paddleocr --upgrade
pip install easyocr --upgrade
pip install pytesseract --upgrade
```

### Issue 2: Tesseract Not Found

**Error**: `TesseractNotFoundError`

**Solution**:
1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR`
3. Add to PATH or set in code:
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Issue 3: pdf2image Poppler Error

**Error**: `PDFInfoNotInstalledError`

**Solution**:
1. Download Poppler: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract to: `C:\poppler`
3. Add to PATH or use in code:
```python
from pdf2image import convert_from_path
images = convert_from_path(pdf_path, poppler_path=r'C:\poppler\bin')
```

### Issue 4: LLM Returns Invalid JSON

**Error**: JSON parsing fails in classification

**Solution**:
- System automatically falls back to manual values
- Check LLM prompt clarity
- Check LLM model temperature settings
- Verify LLM is returning proper JSON format

### Issue 5: No MCQs Extracted

**Error**: Processing completes but 0 MCQs saved

**Solution**:
1. Check OCR text quality (enable debug logging)
2. Verify PDF contains actual MCQ format
3. Check LLM MCQ extraction prompt
4. Test with different page ranges
5. Try different OCR engine

## Test Data

### Sample Math Problems for Testing

**Algebra**:
- Linear equations
- Quadratic equations
- Polynomials

**Geometry**:
- Triangles and circles
- Area and perimeter
- 3D shapes

**Trigonometry**:
- Sin, cos, tan
- Trigonometric identities
- Angles and radians

### Sample PDF Structure

Ideal test PDF should have:
- Clear MCQ format with A/B/C/D options
- Mixed difficulty levels
- Multiple chapters
- Page numbers
- Readable fonts
- Minimal diagrams (for OCR accuracy)

## Success Criteria

✅ **Basic Functionality**
- PDF upload works
- GO button appears and links correctly
- Form displays and validates
- OCR extracts text
- LLM classifies chapter and difficulty
- MCQs extracted and saved
- ProcessingLog created

✅ **Error Handling**
- Invalid inputs caught by validation
- OCR failures handled gracefully
- LLM failures fall back to manual values
- Database errors don't crash system

✅ **Performance**
- Single page: < 10 seconds
- 10-page range: < 2 minutes
- 100-page PDF: < 20 minutes
- No memory leaks
- Handles concurrent requests

✅ **Regression**
- Expression mode still works
- Existing admin actions work
- LaTeX conversion works
- MCQ generation works

## Next Steps After Testing

1. **Production Deployment**:
   - Review logs from test runs
   - Optimize slow operations
   - Set up monitoring
   - Configure error alerts

2. **User Training**:
   - Document admin workflow
   - Create video tutorial
   - Share best practices
   - Collect feedback

3. **Enhancements**:
   - Add bulk PDF upload
   - Add PDF preview in admin
   - Add MCQ review interface
   - Add batch chapter classification

The system is ready for comprehensive testing!
