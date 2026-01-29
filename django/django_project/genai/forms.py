"""
Forms for Math Problem Generation PDF Processing
"""

from django import forms
from genai.models import MathProblemGeneration


class MathPDFProcessingForm(forms.Form):
    """Form for configuring PDF-based math MCQ generation"""
    
    # LLM Decision Controls
    chapter_decide_by_llm = forms.BooleanField(
        required=False,
        initial=False,
        label="Let LLM Decide Chapter",
        help_text="If checked, LLM will classify the chapter automatically"
    )
    
    difficulty_level_decide_by_llm = forms.BooleanField(
        required=False,
        initial=False,
        label="Let LLM Decide Difficulty",
        help_text="If checked, LLM will determine difficulty level"
    )
    
    # OCR Engine Selection
    use_paddle_ocr = forms.BooleanField(
        required=False,
        initial=False,
        label="Use PaddleOCR",
        help_text="⚠️ Has DLL issues - requires Visual C++ Redistributable (see OCR_INSTALLATION_STATUS.md)"
    )
    
    use_easy_ocr = forms.BooleanField(
        required=False,
        initial=False,
        label="Use EasyOCR",
        help_text="⚠️ Has DLL issues - requires Visual C++ Redistributable (see OCR_INSTALLATION_STATUS.md)"
    )
    
    use_tesseract = forms.BooleanField(
        required=False,
        initial=True,
        label="Use Tesseract OCR (Recommended)",
        help_text="✅ Works reliably - Traditional OCR engine for text extraction"
    )
    
    # PDF Processing Mode
    process_pdf = forms.BooleanField(
        required=False,
        initial=True,
        label="Process PDF",
        help_text="If checked, PDF will be processed. If unchecked, expression field will be used"
    )
    
    # Page Controls
    page_from = forms.IntegerField(
        required=False,
        initial=1,
        min_value=1,
        label="Page From",
        help_text="Starting page number (1 = first page, 2 = second page, etc.)"
    )
    
    page_to = forms.IntegerField(
        required=False,
        initial=0,
        min_value=0,
        label="Page To",
        help_text="Ending page number (0 = last page, or specify page number)"
    )
    
    # MCQ Extraction Modes
    process_all_the_mcq_of_the_pageRange = forms.BooleanField(
        required=False,
        initial=False,
        label="Extract All MCQs from Page Range",
        help_text="Extract all MCQs between page_from and page_to"
    )
    
    no_of_pages_at_a_time_For_EntirePDF = forms.IntegerField(
        required=False,
        initial=2,
        min_value=1,
        max_value=10,
        label="Pages per Chunk",
        help_text="Number of pages to process at a time when processing entire PDF"
    )
    
    process_all_the_mcq_all_pages = forms.BooleanField(
        required=False,
        initial=False,
        label="Process Entire PDF",
        help_text="Process all pages in chunks (ignores page_from/page_to)"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        process_pdf = cleaned_data.get('process_pdf')
        use_paddle = cleaned_data.get('use_paddle_ocr')
        use_easy = cleaned_data.get('use_easy_ocr')
        use_tess = cleaned_data.get('use_tesseract')
        
        # If processing PDF, at least one OCR engine must be selected
        if process_pdf:
            if not (use_paddle or use_easy or use_tess):
                raise forms.ValidationError(
                    "At least one OCR engine must be selected when processing PDF"
                )
        
        # Validate page range
        page_from = cleaned_data.get('page_from', 0)
        page_to = cleaned_data.get('page_to', 0)
        
        if page_from and page_to and page_from > page_to:
            raise forms.ValidationError(
                "Page From cannot be greater than Page To"
            )
        
        return cleaned_data
