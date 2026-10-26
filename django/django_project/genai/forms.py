"""
Forms for Math Problem Generation PDF Processing
"""

from django import forms
from django.forms import formset_factory
from genai.models import MathProblemGeneration
from bank.models import MATH_CHAPTER_CHOICES, RULE_NAME_CHOICES


class MathPromptGenerationForm(forms.Form):
    """Top-level form: the master prompt (pasted or loaded from a saved template) + the PDF
    to run it against."""

    saved_prompt = forms.ChoiceField(
        label="Load a saved prompt",
        required=False,
        help_text="Pick a previously saved prompt to fill the box below, or write/edit it directly."
    )
    prompt_text = forms.CharField(
        label="Your prompt",
        widget=forms.Textarea(attrs={'rows': 16, 'style': 'width:100%;font-family:monospace;font-size:12px;'}),
        help_text="Paste your full extraction prompt here. Use {difficulty} as a placeholder — it will be "
                   "substituted per row below."
    )
    save_prompt_as = forms.CharField(
        label="Save this prompt as",
        required=False,
        max_length=150,
        help_text="Optional. Give it a name to save/update it as a reusable template for next time."
    )
    make_default_prompt = forms.BooleanField(
        label="Make this the default (auto-fill on page load)",
        required=False,
    )
    llm_provider = forms.ChoiceField(
        label="LLM Provider",
        choices=[('', '— use site default —'), ('groq', 'Groq'), ('gemini', 'Gemini'),
                 ('openai', 'OpenAI'), ('deepseek', 'DeepSeek'), ('nvidia', 'NVIDIA NIM')],
        required=False,
        help_text="Which LLM to send each row's prompt to. Leave as default to use the site-wide setting."
    )
    delay_seconds = forms.IntegerField(
        label="Delay between rows (seconds)",
        initial=20,
        min_value=0,
        required=False,
        help_text="Pause this long after each row finishes before starting the next row's LLM call "
                   "(rows still run one at a time either way)."
    )
    pdf_file = forms.FileField(label="Source PDF")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from genai.models import MathPromptTemplate
        choices = [('', '— none —')] + [
            (t.name, t.name) for t in MathPromptTemplate.objects.all()
        ]
        self.fields['saved_prompt'].choices = choices


class MathPromptRowForm(forms.Form):
    """One chapter/rule/page-range row. One LLM call is made per row."""

    chapter = forms.ChoiceField(choices=MATH_CHAPTER_CHOICES)
    rule_name = forms.ChoiceField(
        choices=[('', '— All rules in this range —')] + list(RULE_NAME_CHOICES),
        required=False,
    )
    page_from = forms.IntegerField(min_value=1)
    page_to = forms.IntegerField(min_value=1)
    difficulty = forms.ChoiceField(
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        initial='medium',
    )

    def clean(self):
        cleaned = super().clean()
        page_from = cleaned.get('page_from')
        page_to = cleaned.get('page_to')
        if page_from and page_to and page_to < page_from:
            raise forms.ValidationError("Page to must be >= page from.")
        return cleaned


MathPromptRowFormSet = formset_factory(MathPromptRowForm, extra=1, can_delete=True)


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

    # Extract Rule Mode
    extract_rule = forms.BooleanField(
        required=False,
        initial=False,
        label="Extract Rule (instead of MCQs)",
        help_text="When checked, extracts rule theorem/content from the PDF and saves it to the rule_math table"
    )

    rule_number = forms.ChoiceField(
        required=False,
        label="Rule Number",
        help_text="Select which rule number this PDF page corresponds to"
    )

    # Prompt Selection
    pdf_prompt = forms.ChoiceField(
        required=False,
        label="Prompt for PDF Processing",
        help_text="Select which LLMPrompt to use when extracting MCQs from PDF"
    )

    expression_prompt = forms.ChoiceField(
        required=False,
        label="Prompt for Expression Processing",
        help_text="Select which LLMPrompt to use when processing an expression/text"
    )

    def __init__(self, *args, **kwargs):
        prompt_choices = kwargs.pop('prompt_choices', [])
        rule_choices = kwargs.pop('rule_choices', [('', '— Select Rule —')])
        super().__init__(*args, **kwargs)
        self.fields['pdf_prompt'].choices = prompt_choices
        self.fields['expression_prompt'].choices = prompt_choices
        self.fields['rule_number'].choices = rule_choices

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
