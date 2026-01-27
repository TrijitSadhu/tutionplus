"""
Subject-Specific Processors
Extend SubjectMCQGenerator for different subjects
"""

from genai.tasks.pdf_processor import SubjectMCQGenerator
from genai.models import LLMPrompt
import logging

logger = logging.getLogger(__name__)


class SubjectSpecificProcessor(SubjectMCQGenerator):
    """Base class for subject-specific processors"""
    
    SUBJECT_NAME = None
    SUBJECT_SLUG = None
    
    def __init__(self, *args, **kwargs):
        print(f"\n{'─'*80}")
        print(f"[PROCESSOR] {self.__class__.__name__}.__init__()")
        print(f"  SUBJECT_NAME: {self.SUBJECT_NAME}")
        print(f"  SUBJECT_SLUG: {self.SUBJECT_SLUG}")
        super().__init__(*args, **kwargs)
    
    def get_subject_specific_prompt(self, prompt_type: str = 'mcq') -> str:
        """Get subject-specific prompt from database"""
        print(f"\n{'─'*80}")
        print(f"[PROCESSOR] {self.__class__.__name__}.get_subject_specific_prompt()")
        print(f"  INPUT: prompt_type={prompt_type}")
        
        try:
            source_url = f"pdf_{self.SUBJECT_SLUG}_{prompt_type}"
            print(f"  SEARCHING: source_url={source_url}")
            
            prompt = LLMPrompt.objects.get(
                source_url=source_url,
                prompt_type=prompt_type,
                is_active=True
            )
            print(f"  ✅ FOUND: LLMPrompt ID={prompt.id}")
            print(f"  OUTPUT: prompt_text length={len(prompt.prompt_text)} chars\n")
            return prompt.prompt_text
            
        except LLMPrompt.DoesNotExist:
            print(f"  ❌ NOT FOUND: Using default prompt")
            default_prompt = self.generate_mcq_prompt(
                chapter=self.SUBJECT_NAME,
                topic="General",
                content="",
                num_questions=5
            )
            print(f"  OUTPUT: default_prompt length={len(default_prompt)} chars\n")
            return default_prompt


class PolityProcessor(SubjectSpecificProcessor):
    """Process PDFs for Polity"""
    SUBJECT_NAME = "Polity"
    SUBJECT_SLUG = "polity"


class EconomicsProcessor(SubjectSpecificProcessor):
    """Process PDFs for Economics"""
    SUBJECT_NAME = "Economics"
    SUBJECT_SLUG = "economics"


class MathProcessor(SubjectSpecificProcessor):
    """Process PDFs for Mathematics"""
    SUBJECT_NAME = "Mathematics"
    SUBJECT_SLUG = "math"


class PhysicsProcessor(SubjectSpecificProcessor):
    """Process PDFs for Physics"""
    SUBJECT_NAME = "Physics"
    SUBJECT_SLUG = "physics"


class ChemistryProcessor(SubjectSpecificProcessor):
    """Process PDFs for Chemistry"""
    SUBJECT_NAME = "Chemistry"
    SUBJECT_SLUG = "chemistry"


class HistoryProcessor(SubjectSpecificProcessor):
    """Process PDFs for History"""
    SUBJECT_NAME = "History"
    SUBJECT_SLUG = "history"


class GeographyProcessor(SubjectSpecificProcessor):
    """Process PDFs for Geography"""
    SUBJECT_NAME = "Geography"
    SUBJECT_SLUG = "geography"


class BiologyProcessor(SubjectSpecificProcessor):
    """Process PDFs for Biology"""
    SUBJECT_NAME = "Biology"
    SUBJECT_SLUG = "biology"
