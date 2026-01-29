"""
Math LaTeX Processing Task Module
Converts math problems and questions into LaTeX format with MCQs
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple

from genai.utils.llm_provider import default_llm

logger = logging.getLogger(__name__)


class LaTeXConverter:
    """Converts math expressions to LaTeX format"""
    
    def __init__(self):
        self.llm = default_llm
    
    @staticmethod
    def is_latex_formatted(text: str) -> bool:
        """Check if text is already LaTeX formatted"""
        return bool(re.search(r'\$.*\$|\\\w+|\{.*\}', text))
    
    def generate_latex_conversion_prompt(self, math_content: str) -> str:
        """Generate prompt for LaTeX conversion"""
        return f"""
You are an expert in mathematical notation and LaTeX.
Convert the following mathematical expression/problem into proper LaTeX format.

Input: {math_content}

Rules:
1. Use $...$ for inline math
2. Use \\[...\\] for display math
3. Use proper LaTeX commands for mathematical symbols
4. Preserve all mathematical relationships
5. Add proper spacing and formatting

Return ONLY a JSON object with this structure:
{{
    "original": "{math_content}",
    "latex": "LaTeX formatted version",
    "latex_display": "Display math version if applicable",
    "symbols_used": ["list", "of", "symbols"],
    "validation": "Valid LaTeX (Yes/No)"
}}
"""
    
    def convert_to_latex(self, math_content: str) -> Dict[str, Any]:
        """
        Convert mathematical expression to LaTeX
        
        Args:
            math_content: Mathematical expression or problem
        
        Returns:
            Conversion result with LaTeX format
        """
        try:
            # Check if already LaTeX formatted
            if self.is_latex_formatted(math_content):
                logger.info("Content already appears to be LaTeX formatted")
                return {
                    "original": math_content,
                    "latex": math_content,
                    "already_formatted": True
                }
            
            # Use LLM for conversion
            prompt = self.generate_latex_conversion_prompt(math_content)
            response = self.llm.generate_json(prompt)
            
            return response
        
        except Exception as e:
            logger.error(f"Error converting to LaTeX: {str(e)}")
            return {"error": str(e)}


class MathMCQGenerator:
    """Generates MCQs for math problems with LaTeX"""
    
    def __init__(self):
        self.latex_converter = LaTeXConverter()
        self.llm = default_llm
    
    def generate_math_mcq_prompt(self, problem: str, latex_format: str, difficulty: str = "Medium") -> str:
        """Generate prompt for math MCQ creation"""
        return f"""
You are an expert math educator creating competitive exam questions.
Generate 1 high-quality multiple choice question based on the following problem.

Problem: {problem}
LaTeX Format: {latex_format}
Difficulty Level: {difficulty}

Important:
- Create questions that test problem-solving skills
- Options should include common mistakes
- Provide detailed explanations
- Format all math in LaTeX using $ $ for inline math

Return ONLY a JSON object with this structure:
{{
    "problem_latex": "{latex_format}",
    "question": "Question text",
    "option_a": "Option A with LaTeX",
    "option_b": "Option B with LaTeX",
    "option_c": "Option C with LaTeX",
    "option_d": "Option D with LaTeX",
    "correct_answer": "A",
    "explanation": "Detailed solution steps in LaTeX where needed",
    "difficulty": "{difficulty}",
    "concepts_tested": ["concept1", "concept2"]
}}
"""
    
    def process_math_problem(self, problem: str, difficulty: str = "Medium") -> Dict[str, Any]:
        """
        Process math problem and generate MCQ with LaTeX
        
        Args:
            problem: Math problem statement
            difficulty: Problem difficulty level
        
        Returns:
            Generated MCQ with LaTeX formatting
        """
        try:
            # Step 1: Convert to LaTeX
            logger.info("Converting math problem to LaTeX")
            latex_result = self.latex_converter.convert_to_latex(problem)
            
            if "error" in latex_result:
                return latex_result
            
            latex_format = latex_result.get('latex', problem)
            
            # Step 2: Generate MCQ
            logger.info("Generating MCQ for math problem")
            prompt = self.generate_math_mcq_prompt(problem, latex_format, difficulty)
            mcq_response = self.llm.generate_json(prompt)
            
            # Add LaTeX conversion info to response
            mcq_response['latex_conversion'] = latex_result
            
            return mcq_response
        
        except Exception as e:
            logger.error(f"Error processing math problem: {str(e)}")
            return {"error": str(e)}
    
    def process_math_chapter(self, chapter_name: str, problems: List[str], 
                            difficulty: str = "Medium") -> Dict[str, Any]:
        """
        Process multiple math problems from a chapter
        
        Args:
            chapter_name: Name of math chapter
            problems: List of math problems
            difficulty: Difficulty level
        
        Returns:
            List of generated MCQs
        """
        results = {
            "chapter": chapter_name,
            "total_problems": len(problems),
            "processed_mcqs": [],
            "errors": []
        }
        
        for i, problem in enumerate(problems, 1):
            try:
                logger.info(f"Processing problem {i}/{len(problems)}")
                mcq = self.process_math_problem(problem, difficulty)
                
                if "error" not in mcq:
                    results["processed_mcqs"].append(mcq)
                else:
                    results["errors"].append(f"Problem {i}: {mcq['error']}")
            
            except Exception as e:
                logger.error(f"Error processing problem {i}: {str(e)}")
                results["errors"].append(f"Problem {i}: {str(e)}")
        
        return results
    
    def save_math_mcqs_to_database(self, mcq_data: Dict[str, Any]) -> List[Dict]:
        """
        Save generated math MCQs to database
        Note: Adjust based on your actual math model
        
        Args:
            mcq_data: MCQ data from LLM
        
        Returns:
            List of saved item IDs
        """
        saved_items = []
        
        try:
            # Import your math model
            # from bank.models import Math  # Adjust based on your model
            
            # Placeholder - adjust based on your math model structure
            saved_items.append({
                'id': 'math_' + str(hash(mcq_data.get('question', '')))[-8:],
                'problem_latex': mcq_data.get('problem_latex', ''),
                'question': mcq_data.get('question', '')
            })
            
            logger.info(f"Saved math MCQ: {saved_items[-1]['id']}")
        
        except Exception as e:
            logger.error(f"Error saving to math table: {str(e)}")
        
        return saved_items


class MathParser:
    """Parses and validates mathematical expressions"""
    
    @staticmethod
    def extract_formulas(text: str) -> List[str]:
        """Extract mathematical formulas from text"""
        # Extract content between $ ... $
        inline = re.findall(r'\$([^$]+)\$', text)
        # Extract content between \[ ... \]
        display = re.findall(r'\\\[([^\]]+)\\\]', text)
        return inline + display
    
    @staticmethod
    def validate_latex_syntax(latex_str: str) -> Tuple[bool, Optional[str]]:
        """
        Basic LaTeX syntax validation
        
        Args:
            latex_str: LaTeX string to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for unmatched braces
        open_braces = latex_str.count('{')
        close_braces = latex_str.count('}')
        if open_braces != close_braces:
            return False, "Unmatched braces"
        
        # Check for unmatched dollar signs
        dollar_count = latex_str.count('$')
        if dollar_count % 2 != 0:
            return False, "Unmatched dollar signs"
        
        return True, None


def process_math_problem(problem: str, difficulty: str = "Medium") -> Dict[str, Any]:
    """
    Convenience function to process math problem
    
    Args:
        problem: Math problem statement
        difficulty: Difficulty level
    
    Returns:
        Generated MCQ with LaTeX
    """
    generator = MathMCQGenerator()
    return generator.process_math_problem(problem, difficulty)


def batch_process_math_problems(problems: List[str], chapter: str = "General", 
                               difficulty: str = "Medium") -> Dict[str, Any]:
    """
    Convenience function for batch processing
    
    Args:
        problems: List of math problems
        chapter: Chapter name
        difficulty: Difficulty level
    
    Returns:
        Batch processing results
    """
    generator = MathMCQGenerator()
    return generator.process_math_chapter(chapter, problems, difficulty)


# ============================================================================
# OCR ENGINES FOR PDF PROCESSING
# ============================================================================

class OCREngine:
    """Base class for OCR engines"""
    
    def __init__(self):
        self.name = "Base OCR"
    
    def extract_text(self, pdf_path: str, page_num: int = 0) -> Optional[str]:
        """Extract text from PDF page"""
        raise NotImplementedError


class PaddleOCREngine(OCREngine):
    """PaddleOCR engine - High accuracy for Chinese and English"""
    
    _instance = None
    _ocr = None
    
    def __new__(cls):
        """Singleton pattern to avoid reinitialization"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.name = "PaddleOCR"
            self.initialized = True
    
    def _initialize(self):
        """Lazy initialization of PaddleOCR (singleton)"""
        if PaddleOCREngine._ocr is None:
            try:
                from paddleocr import PaddleOCR
                PaddleOCREngine._ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
                logger.info("[PaddleOCR] Initialized successfully")
            except ImportError:
                logger.error("[PaddleOCR] Not installed. Install with: pip install paddleocr")
                raise
            except Exception as e:
                logger.error(f"[PaddleOCR] Initialization error: {e}")
                raise
    
    def extract_text(self, pdf_path: str, page_num: int = 0) -> Optional[str]:
        """Extract text using PaddleOCR with PyMuPDF (no Poppler needed)"""
        try:
            self._initialize()
            
            import fitz  # PyMuPDF
            import tempfile
            
            logger.info(f"[PaddleOCR] Processing page {page_num} of {pdf_path}")
            
            # Open PDF with PyMuPDF
            pdf_document = fitz.open(pdf_path)
            
            if page_num >= len(pdf_document):
                logger.error(f"[PaddleOCR] Page {page_num} does not exist (total pages: {len(pdf_document)})")
                pdf_document.close()
                return None
            
            # Get the specific page and convert to image
            page = pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                pix.save(tmp.name)
                temp_image_path = tmp.name
            
            pdf_document.close()
            
            # Run OCR
            result = PaddleOCREngine._ocr.ocr(temp_image_path, cls=True)
            
            # Extract text
            text_lines = []
            if result and result[0]:
                for line in result[0]:
                    if line[1][0]:  # line[1][0] is the text
                        text_lines.append(line[1][0])
            
            extracted_text = '\n'.join(text_lines)
            
            logger.info(f"[PaddleOCR] Extracted {len(extracted_text)} characters")
            
            # Cleanup
            import os
            try:
                os.remove(temp_image_path)
            except:
                pass
            
            return extracted_text if extracted_text else None
            
        except ImportError as e:
            logger.error(f"[PaddleOCR] Import error: {e}")
            return None
        except Exception as e:
            logger.error(f"[PaddleOCR] Extraction error: {e}")
            import traceback
            traceback.print_exc()
            return None


class EasyOCREngine(OCREngine):
    """EasyOCR engine - Supports 80+ languages"""
    
    _instance = None
    _reader = None
    
    def __new__(cls):
        """Singleton pattern to avoid reinitialization"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.name = "EasyOCR"
            self.initialized = True
    
    def _initialize(self):
        """Lazy initialization of EasyOCR (singleton)"""
        if EasyOCREngine._reader is None:
            try:
                import easyocr
                EasyOCREngine._reader = easyocr.Reader(['en'], gpu=False, verbose=False)
                logger.info("[EasyOCR] Initialized successfully")
            except ImportError:
                logger.error("[EasyOCR] Not installed. Install with: pip install easyocr")
                raise
            except Exception as e:
                logger.error(f"[EasyOCR] Initialization error: {e}")
                raise
    
    def extract_text(self, pdf_path: str, page_num: int = 0) -> Optional[str]:
        """Extract text using EasyOCR with PyMuPDF (no Poppler needed)"""
        try:
            self._initialize()
            
            import fitz  # PyMuPDF
            import numpy as np
            from PIL import Image
            import io
            
            logger.info(f"[EasyOCR] Processing page {page_num} of {pdf_path}")
            
            # Open PDF with PyMuPDF
            pdf_document = fitz.open(pdf_path)
            
            if page_num >= len(pdf_document):
                logger.error(f"[EasyOCR] Page {page_num} does not exist (total pages: {len(pdf_document)})")
                pdf_document.close()
                return None
            
            # Get the specific page and convert to image
            page = pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
            
            # Convert pixmap to PIL Image then to numpy array
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            image_array = np.array(image)
            
            pdf_document.close()
            
            # Run OCR
            result = EasyOCREngine._reader.readtext(image_array, detail=0)
            
            extracted_text = '\n'.join(result)
            
            logger.info(f"[EasyOCR] Extracted {len(extracted_text)} characters")
            
            return extracted_text if extracted_text else None
            
        except ImportError as e:
            logger.error(f"[EasyOCR] Import error: {e}")
            return None
        except Exception as e:
            logger.error(f"[EasyOCR] Extraction error: {e}")
            import traceback
            traceback.print_exc()
            return None


class TesseractOCREngine(OCREngine):
    """Tesseract OCR engine - Traditional OCR"""
    
    def __init__(self):
        super().__init__()
        self.name = "Tesseract"
    
    def extract_text(self, pdf_path: str, page_num: int = 0) -> Optional[str]:
        """Extract text using Tesseract OCR with PyMuPDF (no Poppler needed)"""
        try:
            import pytesseract
            import fitz  # PyMuPDF
            from PIL import Image
            import io
            
            # Configure Tesseract path if not in system PATH
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            
            logger.info(f"[Tesseract] Processing page {page_num} of {pdf_path}")
            
            # Open PDF with PyMuPDF
            pdf_document = fitz.open(pdf_path)
            
            if page_num >= len(pdf_document):
                logger.error(f"[Tesseract] Page {page_num} does not exist (total pages: {len(pdf_document)})")
                pdf_document.close()
                return None
            
            # Get the specific page
            page = pdf_document[page_num]
            
            # Convert page to image (pixmap)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
            
            # Convert pixmap to PIL Image
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            # Close PDF
            pdf_document.close()
            
            # Run OCR
            extracted_text = pytesseract.image_to_string(image)
            
            logger.info(f"[Tesseract] Extracted {len(extracted_text)} characters")
            
            return extracted_text if extracted_text else None
            
        except ImportError as e:
            logger.error(f"[Tesseract] Import error: {e}. Install with: pip install pytesseract PyMuPDF Pillow")
            return None
        except Exception as e:
            logger.error(f"[Tesseract] Extraction error: {e}")
            import traceback
            traceback.print_exc()
            return None


class OCRDispatcher:
    """Dispatcher to select and run OCR engines with fallback"""
    
    def __init__(self, use_paddle: bool = True, use_easy: bool = True, use_tesseract: bool = True):
        self.engines = []
        
        if use_paddle:
            self.engines.append(PaddleOCREngine())
        if use_easy:
            self.engines.append(EasyOCREngine())
        if use_tesseract:
            self.engines.append(TesseractOCREngine())
        
        if not self.engines:
            raise ValueError("At least one OCR engine must be enabled")
        
        logger.info(f"[OCR Dispatcher] Initialized with engines: {[e.name for e in self.engines]}")
    
    def extract_text(self, pdf_path: str, page_num: int = 0) -> Optional[str]:
        """
        Extract text using direct extraction first, then fallback to OCR
        Priority: Direct Text Extraction → PaddleOCR → EasyOCR → Tesseract
        """
        print(f"\n{'='*80}")
        print(f"[TEXT EXTRACTION] Starting for page {page_num}")
        print(f"[TEXT EXTRACTION] Method: OCRDispatcher.extract_text()")
        print(f"[TEXT EXTRACTION] Available OCR engines: {[e.name for e in self.engines]}")
        print(f"{'='*80}\n")
        
        # STEP 1: Try direct text extraction first (fast, no OCR needed)
        try:
            import fitz  # PyMuPDF
            print(f"[STEP 1] Attempting DIRECT TEXT EXTRACTION (no OCR)")
            logger.info(f"[OCR Dispatcher] Trying direct text extraction first...")
            
            pdf_document = fitz.open(pdf_path)
            if page_num < len(pdf_document):
                page = pdf_document[page_num]
                direct_text = page.get_text()
                pdf_document.close()
                
                if direct_text and len(direct_text.strip()) > 50:  # At least 50 chars
                    print(f"✅ [DIRECT EXTRACTION] SUCCESS - Extracted {len(direct_text)} characters")
                    print(f"[DIRECT EXTRACTION] OCR NOT NEEDED - Text-based PDF\n")
                    logger.info(f"[OCR Dispatcher] ✅ Direct extraction succeeded ({len(direct_text)} chars)")
                    return direct_text
                else:
                    print(f"⚠️  [DIRECT EXTRACTION] Minimal text found ({len(direct_text.strip()) if direct_text else 0} chars)")
                    print(f"[DIRECT EXTRACTION] Proceeding to OCR extraction...\n")
                    logger.info(f"[OCR Dispatcher] Direct extraction returned minimal text, trying OCR...")
            else:
                pdf_document.close()
        except Exception as e:
            logger.warning(f"[OCR Dispatcher] Direct extraction failed: {e}, trying OCR...")
        
        # STEP 2: Fallback to OCR engines
        print(f"[STEP 2] DIRECT EXTRACTION FAILED - Using OCR Engines")
        for idx, engine in enumerate(self.engines, 1):
            print(f"\n[OCR Engine {idx}/{len(self.engines)}] Trying: {engine.name}")
            logger.info(f"[OCR Dispatcher] Trying {engine.name}...")
            
            try:
                text = engine.extract_text(pdf_path, page_num)
                
                if text and len(text.strip()) > 0:
                    print(f"✅ [OCR {engine.name}] SUCCESS - Extracted {len(text)} characters")
                    logger.info(f"[OCR Dispatcher] ✅ {engine.name} succeeded")
                    return text
                else:
                    print(f"❌ [OCR {engine.name}] FAILED - No text extracted")
                    logger.warning(f"[OCR Dispatcher] {engine.name} returned empty text")
            
            except Exception as e:
                logger.error(f"[OCR Dispatcher] {engine.name} failed: {e}")
                continue
        
        logger.error("[OCR Dispatcher] ❌ All extraction methods failed")
        return None


# ============================================================================
# PDF PROCESSOR WITH LLM-CONTROLLED ROUTING
# ============================================================================

class MathPDFProcessor:
    """Process math PDFs with OCR and LLM-controlled routing"""
    
    def __init__(self):
        self.llm = default_llm
        self.latex_converter = LaTeXConverter()
        self.mcq_generator = MathMCQGenerator()
        logger.info("[MathPDFProcessor] Initialized")
    
    def get_or_create_chapter_classification_prompt(self) -> str:
        """Get or create LLM prompt for chapter classification"""
        from genai.models import LLMPrompt, MathProblemGeneration
        
        print(f"\n[PROMPT FETCH] Method: get_or_create_chapter_classification_prompt()")
        print(f"[PROMPT FETCH] Looking for: prompt_type='descriptive', is_default=True")
        
        # Try to get existing default prompt for math classification
        try:
            prompt_obj = LLMPrompt.objects.filter(
                prompt_type='descriptive',
                is_default=True,
                is_active=True
            ).first()
            
            if prompt_obj:
                print(f"✅ [PROMPT FETCH] Found existing prompt in database")
                print(f"[PROMPT] ID: {prompt_obj.id}")
                print(f"[PROMPT] Type: {prompt_obj.prompt_type}")
                print(f"[PROMPT] Is Default: {prompt_obj.is_default}")
                print(f"[PROMPT] Source URL: {prompt_obj.source_url or 'Default'}")
                logger.info("[Chapter Classification] Using existing prompt")
                return prompt_obj.prompt_text
            else:
                print(f"⚠️ [PROMPT FETCH] No default prompt found in database")
        except Exception as e:
            print(f"❌ [PROMPT FETCH] Error fetching prompt: {e}")
            logger.warning(f"[Chapter Classification] Error fetching prompt: {e}")
        
        # Create new prompt
        chapter_choices = MathProblemGeneration.get_chapter_choices()
        chapter_list = ', '.join([ch[0] for ch in chapter_choices])
        
        default_prompt = f"""You are an expert in mathematics chapter classification.
Analyze the given math problem and determine which chapter it belongs to.

Available Chapters: {chapter_list}

Problem Content:
{{content}}

Return ONLY a JSON object with this structure:
{{
    "chapter": "chapter_name",
    "confidence": 0.95,
    "reasoning": "Brief explanation of why this chapter"
}}

Rules:
- chapter must be one of the available chapters
- confidence should be between 0 and 1
- If unsure, use the most relevant chapter
"""
        
        # Try to save it as default prompt
        try:
            from genai.models import LLMPrompt
            # Check if a default already exists
            existing_default = LLMPrompt.objects.filter(
                prompt_type='descriptive',
                is_default=True
            ).first()
            
            if not existing_default:
                prompt_obj = LLMPrompt.objects.create(
                    prompt_type='descriptive',
                    prompt_text=default_prompt,
                    is_default=True,
                    is_active=True
                )
                print(f"✅ [PROMPT] Saved new default prompt to database (ID: {prompt_obj.id})")
                logger.info("[Chapter Classification] Created new default prompt")
            else:
                print(f"⚠️ [PROMPT] Default prompt already exists (ID: {existing_default.id}), using that")
        except Exception as e:
            print(f"⚠️ [PROMPT] Could not save to database: {e}")
            logger.warning(f"[Chapter Classification] Could not save prompt: {e}")
        
        return default_prompt
    
    def classify_chapter_by_llm(self, content: str) -> Dict[str, Any]:
        """Use LLM to classify chapter"""
        try:
            print(f"\n{'='*80}")
            print(f"[CHAPTER CLASSIFICATION] Using LLM")
            print(f"{'='*80}\n")
            
            prompt_template = self.get_or_create_chapter_classification_prompt()
            prompt = prompt_template.replace('{content}', content[:2000])  # Limit content
            
            response = self.llm.generate_json(prompt)
            
            if response and 'chapter' in response:
                print(f"[CHAPTER] LLM classified as: {response['chapter']}")
                print(f"[CHAPTER] Confidence: {response.get('confidence', 'N/A')}")
                print(f"[CHAPTER] Reasoning: {response.get('reasoning', 'N/A')}\n")
                return response
            else:
                logger.error("[CHAPTER] Invalid LLM response")
                return {'chapter': 'any', 'confidence': 0.5, 'reasoning': 'LLM returned invalid format'}
        
        except Exception as e:
            logger.error(f"[CHAPTER] Classification error: {e}")
            return {'chapter': 'any', 'confidence': 0.0, 'reasoning': f'Error: {str(e)}'}
    
    def classify_difficulty_by_llm(self, content: str) -> Dict[str, Any]:
        """Use LLM to classify difficulty"""
        try:
            print(f"\n{'='*80}")
            print(f"[DIFFICULTY CLASSIFICATION] Using LLM")
            print(f"{'='*80}\n")
            
            prompt = f"""You are an expert in math problem difficulty assessment.
Analyze the given math problem and determine its difficulty level.

Problem Content:
{content[:2000]}

Return ONLY a JSON object with this structure:
{{
    "difficulty": "easy|medium|hard",
    "confidence": 0.95,
    "reasoning": "Brief explanation of why this difficulty"
}}

Difficulty Guidelines:
- easy: Basic arithmetic, simple equations, direct application
- medium: Multi-step problems, moderate complexity, requires thinking
- hard: Complex problems, advanced concepts, multiple techniques
"""
            
            response = self.llm.generate_json(prompt)
            
            if response and 'difficulty' in response:
                print(f"[DIFFICULTY] LLM classified as: {response['difficulty']}")
                print(f"[DIFFICULTY] Confidence: {response.get('confidence', 'N/A')}")
                print(f"[DIFFICULTY] Reasoning: {response.get('reasoning', 'N/A')}\n")
                return response
            else:
                logger.error("[DIFFICULTY] Invalid LLM response")
                return {'difficulty': 'medium', 'confidence': 0.5, 'reasoning': 'LLM returned invalid format'}
        
        except Exception as e:
            logger.error(f"[DIFFICULTY] Classification error: {e}")
            return {'difficulty': 'medium', 'confidence': 0.0, 'reasoning': f'Error: {str(e)}'}
    
    def get_or_create_mcq_extraction_prompt(self) -> str:
        """Get or create LLM prompt for MCQ extraction from PDF text"""
        from genai.models import LLMPrompt
        
        print(f"\n[PROMPT FETCH] Method: get_or_create_mcq_extraction_prompt()")
        print(f"[PROMPT FETCH] Looking for: source_url='http://pdfmcqprompt.com'")
        
        # Try to get existing MCQ prompt for PDF processing
        try:
            prompt_obj = LLMPrompt.objects.filter(
                source_url='http://pdfmcqprompt.com',
                is_active=True
            ).first()
            
            if prompt_obj:
                print(f"✅ [PROMPT FETCH] Found existing prompt in database")
                print(f"[PROMPT] ID: {prompt_obj.id}")
                print(f"[PROMPT] Type: {prompt_obj.prompt_type}")
                print(f"[PROMPT] Is Default: {prompt_obj.is_default}")
                print(f"[PROMPT] Source URL: {prompt_obj.source_url}")
                print(f"[PROMPT] Is Active: {prompt_obj.is_active}")
                
                # Check if prompt has correct placeholders for math extraction
                prompt_text = prompt_obj.prompt_text
                has_math_placeholders = '{text}' in prompt_text and '{chapter}' in prompt_text and '{difficulty}' in prompt_text
                has_old_placeholders = '{title}' in prompt_text or '{content}' in prompt_text
                
                if has_math_placeholders and not has_old_placeholders:
                    print(f"✅ [PROMPT] Prompt has correct math placeholders")
                    logger.info("[MCQ Extraction] Using existing math prompt from database")
                    return prompt_text
                else:
                    print(f"⚠️ [PROMPT] Prompt has wrong placeholders (current affairs format)")
                    print(f"[PROMPT] Will update to math-specific format")
                    # Fall through to update the prompt
            else:
                print(f"⚠️ [PROMPT FETCH] No prompt found with source_url='http://pdfmcqprompt.com'")
                prompt_obj = None  # Will create new one below
        except Exception as e:
            print(f"❌ [PROMPT FETCH] Error fetching prompt: {e}")
            logger.warning(f"[MCQ Extraction] Error fetching prompt: {e}")
            prompt_obj = None
        
        # Create default prompt
        print(f"[PROMPT] Creating default MCQ extraction prompt for math problems")
        default_prompt = """You are an expert in extracting and creating high-quality mathematics MCQs from textbook content.

Your task is to extract ALL multiple choice questions from the following math content, OR if the content contains problems without proper MCQ format, convert them into well-structured MCQs.

Content:
{text}

Chapter: {chapter}
Difficulty: {difficulty}

CRITICAL REQUIREMENTS:
1. **LaTeX Formatting**: ALWAYS use LaTeX for ALL mathematical expressions, formulas, equations, and symbols
   - Inline math: Use \\( \\) for inline expressions like \\( x^2 + y^2 = z^2 \\)
   - Block math: Use \\[ \\] for displayed equations
   - Examples: \\( \\frac{{a}}{{b}} \\), \\( \\sqrt{{x}} \\), \\( \\alpha, \\beta, \\gamma \\)

2. **Minimum 4 Options**: Each question MUST have exactly 4 options (A, B, C, D)
   - If content has fewer options, create additional plausible wrong options
   - Wrong options should be reasonable distractors, not obviously incorrect

3. **Enhanced Explanations**: 
   - If provided explanation is too brief or unclear, EXPAND it significantly
   - Explanation must be step-by-step, detailed, and easy to understand
   - Write for extreme beginners who need every step explained
   - Use LaTeX for all math steps in explanation
   - After mathematical steps, add textual flow to improve understanding
   - Include WHY each step is done, not just WHAT is done

4. **Question Quality**:
   - Question text must be clear and unambiguous
   - Use LaTeX for all math in the question
   - Include necessary context or given values

5. **Output Format**: Return ONLY a valid JSON object (no markdown, no code blocks)

JSON Structure:
{{
    "questions": [
        {{
            "question": "Complete question text with LaTeX: \\\\( formula \\\\)",
            "option_a": "Option A with LaTeX if needed: \\\\( x = 5 \\\\)",
            "option_b": "Option B with LaTeX if needed: \\\\( x = 10 \\\\)",
            "option_c": "Option C with LaTeX if needed: \\\\( x = 15 \\\\)",
            "option_d": "Option D with LaTeX if needed: \\\\( x = 20 \\\\)",
            "correct_answer": "A",
            "explanation": "Step-by-step explanation with LaTeX:\\n\\n**Step 1:** Start by understanding what is given. We have \\\\( a = 5 \\\\) and \\\\( b = 3 \\\\). This means...\\n\\n**Step 2:** Apply the formula \\\\( c = a + b \\\\). We substitute the values: \\\\( c = 5 + 3 = 8 \\\\). We use this formula because...\\n\\n**Step 3:** Verify the answer. Since \\\\( c = 8 \\\\), we can check by...\\n\\n**Textual Understanding:** The reason we add these numbers is because the problem asks for the total. When we combine two quantities, addition is the appropriate operation. This is a fundamental concept in arithmetic that applies whenever we need to find a combined total."
        }}
    ]
}}

IMPORTANT NOTES:
- Extract ALL questions from the content
- If content has problems but no MCQ format, convert them to MCQs with 4 options
- If no extractable/convertible questions found, return {{"questions": []}}
- Ensure ALL mathematical content uses LaTeX notation
- Make explanations extremely detailed for beginners
- Each explanation should have mathematical steps followed by conceptual understanding
"""
        
        # Update existing prompt or create new one
        try:
            if prompt_obj:
                # Update existing prompt with new math-specific format
                print(f"[PROMPT] Updating existing prompt (ID: {prompt_obj.id}) with math format")
                prompt_obj.prompt_text = default_prompt
                prompt_obj.save()
                print(f"✅ [PROMPT] Updated existing prompt to math-specific format")
                logger.info(f"[MCQ Extraction] Updated prompt ID {prompt_obj.id} to math format")
            else:
                # Create new prompt with specific source_url
                print(f"[PROMPT] Creating new MCQ prompt with source_url='http://pdfmcqprompt.com'")
                prompt_obj = LLMPrompt.objects.create(
                    source_url='http://pdfmcqprompt.com',
                    prompt_type='mcq',
                    prompt_text=default_prompt,
                    is_default=False,
                    is_active=True
                )
                print(f"✅ [PROMPT] Saved new MCQ prompt to database (ID: {prompt_obj.id})")
                logger.info("[MCQ Extraction] Created new prompt in database")
        except Exception as e:
            print(f"⚠️ [PROMPT] Could not save/update in database: {e}")
            logger.warning(f"[MCQ Extraction] Could not save prompt: {e}")
        
        return default_prompt
    
    def get_or_create_expression_mcq_prompt(self) -> str:
        """Get or create LLM prompt for MCQ generation from expression (Convert to LaTeX)"""
        from genai.models import LLMPrompt
        
        print(f"\n[PROMPT FETCH] Method: get_or_create_expression_mcq_prompt()")
        print(f"[PROMPT FETCH] Looking for: source_url='http://mcqpromptFOR-MATH-EXPRESSION.com'")
        
        # Try to get existing MCQ prompt for expression processing
        try:
            prompt_obj = LLMPrompt.objects.filter(
                source_url='http://mcqpromptFOR-MATH-EXPRESSION.com',
                is_active=True
            ).first()
            
            if prompt_obj:
                print(f"✅ [PROMPT FETCH] Found existing prompt in database")
                print(f"[PROMPT] ID: {prompt_obj.id}")
                print(f"[PROMPT] Type: {prompt_obj.prompt_type}")
                print(f"[PROMPT] Is Default: {prompt_obj.is_default}")
                print(f"[PROMPT] Source URL: {prompt_obj.source_url}")
                print(f"[PROMPT] Is Active: {prompt_obj.is_active}")
                logger.info("[Expression MCQ] Using existing prompt from database")
                return prompt_obj.prompt_text
            else:
                print(f"⚠️ [PROMPT FETCH] No prompt found with source_url='http://mcqpromptFOR-MATH-EXPRESSION.com'")
                prompt_obj = None
        except Exception as e:
            print(f"❌ [PROMPT FETCH] Error fetching prompt: {e}")
            logger.warning(f"[Expression MCQ] Error fetching prompt: {e}")
            prompt_obj = None
        
        # Create default prompt if not found
        print(f"[PROMPT] Creating default expression MCQ prompt")
        default_prompt = """You are an expert in extracting and creating high-quality mathematics MCQs from textbook content.

Your task is to extract ALL multiple choice questions from the following math content, OR if the content contains problems without proper MCQ format, convert them into well-structured MCQs.

Content:
{text}

Chapter: {chapter}
Difficulty: {difficulty}

CRITICAL REQUIREMENTS:
1. **LaTeX Formatting**: ALWAYS use LaTeX for ALL mathematical expressions, formulas, equations, and symbols
   - Inline math: Use \\( \\) for inline expressions like \\( x^2 + y^2 = z^2 \\)
   - Block math: Use \\[ \\] for displayed equations
   - Examples: \\( \\frac{{a}}{{b}} \\), \\( \\sqrt{{x}} \\), \\( \\alpha, \\beta, \\gamma \\)

2. **Minimum 4 Options**: Each question MUST have exactly 4 options (A, B, C, D)
   - If content has fewer options, create additional plausible wrong options
   - Wrong options should be reasonable distractors, not obviously incorrect

3. **Enhanced Explanations**: 
   - If provided explanation is too brief or unclear, EXPAND it significantly
   - Explanation must be step-by-step, detailed, and easy to understand
   - Write for extreme beginners who need every step explained
   - Use LaTeX for all math steps in explanation
   - After mathematical steps, add textual flow to improve understanding
   - Include WHY each step is done, not just WHAT is done

4. **Question Quality**:
   - Question text must be clear and unambiguous
   - Use LaTeX for all math in the question
   - Include necessary context or given values

5. **Output Format**: Return ONLY a valid JSON object (no markdown, no code blocks)

JSON Structure:
{{
    "questions": [
        {{
            "question": "Complete question text with LaTeX: \\\\( formula \\\\)",
            "option_a": "Option A with LaTeX if needed: \\\\( x = 5 \\\\)",
            "option_b": "Option B with LaTeX if needed: \\\\( x = 10 \\\\)",
            "option_c": "Option C with LaTeX if needed: \\\\( x = 15 \\\\)",
            "option_d": "Option D with LaTeX if needed: \\\\( x = 20 \\\\)",
            "correct_answer": "A",
            "explanation": "Step-by-step explanation with LaTeX:\\n\\n**Step 1:** Start by understanding what is given. We have \\\\( a = 5 \\\\) and \\\\( b = 3 \\\\). This means...\\n\\n**Step 2:** Apply the formula \\\\( c = a + b \\\\). We substitute the values: \\\\( c = 5 + 3 = 8 \\\\). We use this formula because...\\n\\n**Step 3:** Verify the answer. Since \\\\( c = 8 \\\\), we can check by...\\n\\n**Textual Understanding:** The reason we add these numbers is because the problem asks for the total. When we combine two quantities, addition is the appropriate operation. This is a fundamental concept in arithmetic that applies whenever we need to find a combined total."
        }}
    ]
}}

IMPORTANT NOTES:
- Extract ALL questions from the content
- If content has problems but no MCQ format, convert them to MCQs with 4 options
- If no extractable/convertible questions found, return {{"questions": []}}
- Ensure ALL mathematical content uses LaTeX notation
- Make explanations extremely detailed for beginners
- Each explanation should have mathematical steps followed by conceptual understanding
"""
        
        # Try to create new prompt with specific source_url
        try:
            if not prompt_obj:
                print(f"[PROMPT] Creating new expression MCQ prompt with source_url='http://mcqpromptFOR-MATH-EXPRESSION.com'")
                prompt_obj = LLMPrompt.objects.create(
                    source_url='http://mcqpromptFOR-MATH-EXPRESSION.com',
                    prompt_type='mcq',
                    prompt_text=default_prompt,
                    is_default=False,
                    is_active=True
                )
                print(f"✅ [PROMPT] Saved new expression MCQ prompt to database (ID: {prompt_obj.id})")
                logger.info("[Expression MCQ] Created new prompt in database")
        except Exception as e:
            print(f"⚠️ [PROMPT] Could not save to database: {e}")
            logger.warning(f"[Expression MCQ] Could not save prompt: {e}")
        
        return default_prompt
    
    def process_math_problem_with_config(self, math_problem, config: Dict, log_entry) -> Dict[str, Any]:
        """
        Main processing method with full configuration support
        
        Args:
            math_problem: MathProblemGeneration instance
            config: Processing configuration from form
            log_entry: ProcessingLog instance
        
        Returns:
            Processing result dictionary
        """
        try:
            from django.utils import timezone
            import json
            
            print(f"\n{'='*80}")
            print(f"[MATH PDF PROCESSOR] Starting processing")
            print(f"Math Problem ID: {math_problem.id}")
            print(f"{'='*80}\n")
            
            log_entry.status = 'running'
            log_entry.save()
            
            # Determine processing mode
            if config['process_pdf'] and math_problem.pdf_file:
                print("[MODE] PDF Processing Mode\n")
                result = self._process_pdf_mode(math_problem, config, log_entry)
            elif math_problem.expression:
                print("[MODE] Expression Processing Mode (existing logic)\n")
                result = self._process_expression_mode(math_problem, config, log_entry)
            else:
                raise ValueError("No PDF file or expression provided")
            
            # Update log
            if result.get('success'):
                log_entry.status = 'completed'
                log_entry.output_data = json.dumps(result)
                math_problem.status = 'completed'
            else:
                log_entry.status = 'failed'
                log_entry.error_message = result.get('error', 'Unknown error')
                math_problem.status = 'failed'
                math_problem.error_message = result.get('error', 'Unknown error')
            
            math_problem.processed_at = timezone.now()
            math_problem.save()
            log_entry.save()
            
            print(f"\n{'='*80}")
            print(f"[MATH PDF PROCESSOR] Completed with status: {log_entry.status}")
            print(f"{'='*80}\n")
            
            return result
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            
            log_entry.status = 'failed'
            log_entry.error_message = str(e)
            log_entry.save()
            
            math_problem.status = 'failed'
            math_problem.error_message = str(e)
            math_problem.processed_at = timezone.now()
            math_problem.save()
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def _process_expression_mode(self, math_problem, config: Dict, log_entry) -> Dict[str, Any]:
        """Process using expression field with database prompt and LLM decisions"""
        import json
        from bank.models import math as MathModel
        
        print(f"\n[EXPRESSION MODE] Processing math expression")
        print(f"[EXPRESSION MODE] Input: {math_problem.expression[:100]}...")
        
        # Determine chapter (LLM decision or pre-set)
        if config.get('chapter_decide_by_llm', False):
            print(f"\n[CHAPTER] Using LLM to decide chapter")
            chapter_result = self.classify_chapter_by_llm(math_problem.expression)
            chapter = chapter_result.get('chapter', math_problem.chapter or 'general')
            print(f"[CHAPTER] LLM decided: {chapter}")
        else:
            chapter = math_problem.chapter or 'general'
            print(f"[CHAPTER] Using pre-set: {chapter}")
        
        # Determine difficulty (LLM decision or pre-set)
        if config.get('difficulty_level_decide_by_llm', False):
            print(f"\n[DIFFICULTY] Using LLM to decide difficulty")
            difficulty_result = self.classify_difficulty_by_llm(math_problem.expression, chapter)
            difficulty = difficulty_result.get('difficulty', math_problem.difficulty or 'medium')
            print(f"[DIFFICULTY] LLM decided: {difficulty}")
        else:
            difficulty = math_problem.difficulty or 'medium'
            print(f"[DIFFICULTY] Using pre-set: {difficulty}")
        
        # Fetch prompt from database (Expression mode uses different source_url)
        prompt_template = self.get_or_create_expression_mcq_prompt()
        
        # Replace placeholders
        prompt = prompt_template.replace('{text}', math_problem.expression)
        prompt = prompt.replace('{chapter}', chapter)
        prompt = prompt.replace('{difficulty}', difficulty)
        
        print(f"\n[LLM CALL] Sending expression to LLM...")
        print(f"[LLM CALL] Provider: {self.llm.__class__.__name__}")
        print(f"[LLM CALL] Prompt length: {len(prompt)} characters\n")
        
        # Generate MCQs using LLM
        try:
            response = self.llm.generate_json(prompt)
            
            print(f"[LLM RESPONSE] Received response")
            print(f"[LLM RESPONSE] Has 'questions' key: {'questions' in response if response else False}")
            
            if response and 'questions' in response and len(response['questions']) > 0:
                question_count = len(response['questions'])
                print(f"✅ [MCQ EXTRACTION] SUCCESS - Extracted {question_count} MCQ(s)")
                
                # Save first MCQ to MathProblemGeneration
                first_mcq = response['questions'][0]
                math_problem.generated_mcqs = json.dumps(first_mcq, indent=2)
                math_problem.latex_output = first_mcq.get('question', '')  # Store question as latex_output
                
                # Save all MCQs to bank.math table
                saved_count = 0
                for mcq_data in response['questions']:
                    try:
                        MathModel.objects.create(
                            question=mcq_data.get('question', ''),
                            a=mcq_data.get('option_a', ''),
                            b=mcq_data.get('option_b', ''),
                            c=mcq_data.get('option_c', ''),
                            d=mcq_data.get('option_d', ''),
                            ans=self._convert_answer_to_int(mcq_data.get('correct_answer', 'A')),
                            solution=mcq_data.get('explanation', ''),
                            chapter=chapter,
                            difficult_level=difficulty,
                            level=difficulty,
                        )
                        saved_count += 1
                        print(f"    ✓ Saved MCQ to database")
                    except Exception as e:
                        print(f"    ✗ Failed to save MCQ: {e}")
                
                return {
                    'success': True,
                    'mcq_count': saved_count,
                    'mode': 'expression'
                }
            else:
                print(f"❌ [MCQ EXTRACTION] FAILED - No questions returned")
                return {
                    'success': False,
                    'error': 'LLM did not return any questions'
                }
                
        except Exception as e:
            print(f"❌ [MCQ EXTRACTION] ERROR: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def _process_pdf_mode(self, math_problem, config: Dict, log_entry) -> Dict[str, Any]:
        """Process using PDF file with OCR"""
        import json
        from bank.models import math as MathModel
        
        # Initialize OCR
        ocr = OCRDispatcher(
            use_paddle=config['use_paddle_ocr'],
            use_easy=config['use_easy_ocr'],
            use_tesseract=config['use_tesseract']
        )
        
        pdf_path = math_problem.pdf_file.path
        
        # Determine page strategy
        if config['process_all_the_mcq_all_pages']:
            # Process entire PDF in chunks
            print(f"[STRATEGY] Process all pages in chunks of {config['no_of_pages_at_a_time_For_EntirePDF']}\n")
            page_ranges = self._get_chunk_ranges(pdf_path, config['no_of_pages_at_a_time_For_EntirePDF'])
        elif config['process_all_the_mcq_of_the_pageRange']:
            # Process specific page range
            print(f"[STRATEGY] Process page range: {config['page_from']} to {config['page_to']}\n")
            page_ranges = [(config['page_from'], config['page_to'])]
        else:
            # Process single page or default
            print(f"[STRATEGY] Process single page: {config['page_from']}\n")
            page_ranges = [(config['page_from'], config['page_from'])]
        
        all_mcqs = []
        chapter = math_problem.chapter or 'any'  # Initialize with default
        difficulty = math_problem.difficulty  # Initialize with default
        
        for page_start, page_end in page_ranges:
            print(f"\n[PROCESSING] Pages {page_start} to {page_end} (user-facing)")
            
            # Extract text from pages (convert to 0-based for OCR)
            combined_text = ""
            # Convert 1-based user input to 0-based OCR indexing
            ocr_start = max(0, page_start - 1)
            ocr_end = max(0, page_end - 1) if page_end > 0 else page_end
            
            for page_num in range(ocr_start, ocr_end + 1):
                print(f"  [OCR] Page {page_num + 1} (OCR index: {page_num})...")
                text = ocr.extract_text(pdf_path, page_num)
                if text:
                    combined_text += f"\n\n=== Page {page_num + 1} ===\n\n{text}"
            
            if not combined_text:
                print(f"  [WARNING] No text extracted from pages {page_start}-{page_end} (user-facing)")
                continue
            
            print(f"  [EXTRACTED] {len(combined_text)} characters total\n")
            
            # Decide chapter
            print(f"\n[CHAPTER CLASSIFICATION]")
            if config['chapter_decide_by_llm']:
                print(f"[CHAPTER] Mode: LLM-based classification")
                print(f"[CHAPTER] Method: classify_chapter_by_llm()")
                chapter_result = self.classify_chapter_by_llm(combined_text)
                chapter = chapter_result['chapter']
                print(f"[CHAPTER] LLM classified as: {chapter}")
            else:
                chapter = math_problem.chapter or 'any'
                print(f"[CHAPTER] Mode: Manual/Pre-set")
                print(f"[CHAPTER] Value: {chapter}")
            
            print(f"  [CHAPTER] Using: {chapter}\n")
            
            # Decide difficulty
            print(f"\n[DIFFICULTY CLASSIFICATION]")
            if config['difficulty_level_decide_by_llm']:
                print(f"[DIFFICULTY] Mode: LLM-based classification")
                print(f"[DIFFICULTY] Method: classify_difficulty_by_llm()")
                difficulty_result = self.classify_difficulty_by_llm(combined_text)
                difficulty = difficulty_result['difficulty']
                print(f"[DIFFICULTY] LLM classified as: {difficulty}")
            else:
                difficulty = math_problem.difficulty
                print(f"[DIFFICULTY] Mode: Manual/Pre-set")
                print(f"[DIFFICULTY] Value: {difficulty}")
            
            print(f"  [DIFFICULTY] Using: {difficulty}\n")
            
            # Generate MCQs using LLM
            mcqs = self._extract_mcqs_from_text(combined_text, chapter, difficulty)
            
            print(f"  [MCQS] Extracted {len(mcqs)} MCQs\n")
            
            # Save to database
            for mcq in mcqs:
                try:
                    MathModel.objects.create(
                        question=mcq.get('question', ''),
                        a=mcq.get('option_a', ''),
                        b=mcq.get('option_b', ''),
                        c=mcq.get('option_c', ''),
                        d=mcq.get('option_d', ''),
                        ans=self._convert_answer_to_int(mcq.get('correct_answer', 'A')),
                        solution=mcq.get('explanation', ''),
                        chapter=chapter,
                        difficult_level=difficulty,
                        level=difficulty,
                    )
                    all_mcqs.append(mcq)
                    print(f"    ✓ Saved MCQ to database")
                except Exception as e:
                    print(f"    ✗ Error saving MCQ: {e}")
        
        # Check if any MCQs were generated
        if not all_mcqs:
            error_msg = "No MCQs generated. OCR failed to extract text from PDF. Please check:\n"
            error_msg += "1. Enable Tesseract OCR (recommended - works reliably)\n"
            error_msg += "2. PaddleOCR/EasyOCR have DLL issues - see OCR_INSTALLATION_STATUS.md\n"
            error_msg += "3. Ensure PDF contains readable text/images"
            print(f"\n❌ {error_msg}\n")
            return {
                'success': False,
                'error': error_msg,
                'mcq_count': 0
            }
        
        # Store summary in math_problem
        math_problem.generated_mcqs = json.dumps({
            'total_mcqs': len(all_mcqs),
            'chapter': chapter,
            'difficulty': difficulty,
            'pages_processed': len(page_ranges),
            'mcqs': all_mcqs[:5]  # Store first 5 as sample
        }, indent=2)
        
        return {
            'success': True,
            'mcq_count': len(all_mcqs),
            'mode': 'pdf',
            'chapter': chapter,
            'difficulty': difficulty
        }
    
    def _get_chunk_ranges(self, pdf_path: str, chunk_size: int) -> List[Tuple[int, int]]:
        """Get page ranges for chunked processing"""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            ranges = []
            for i in range(0, total_pages, chunk_size):
                start = i
                end = min(i + chunk_size - 1, total_pages - 1)
                ranges.append((start, end))
            
            return ranges
        except Exception as e:
            logger.error(f"Error determining page count: {e}")
            return [(0, 0)]
    
    def _extract_mcqs_from_text(self, text: str, chapter: str, difficulty: str) -> List[Dict]:
        """Extract MCQs from text using LLM"""
        print(f"\n{'='*80}")
        print(f"[MCQ EXTRACTION] Starting LLM-based MCQ extraction")
        print(f"[MCQ EXTRACTION] Method: _extract_mcqs_from_text()")
        print(f"[MCQ EXTRACTION] Chapter: {chapter}")
        print(f"[MCQ EXTRACTION] Difficulty: {difficulty}")
        print(f"[MCQ EXTRACTION] Input text length: {len(text)} characters")
        print(f"[MCQ EXTRACTION] Text preview (first 200 chars): {text[:200]}...")
        print(f"{'='*80}\n")
        
        try:
            # Fetch prompt from database
            prompt_template = self.get_or_create_mcq_extraction_prompt()
            
            # Replace placeholders in template
            prompt = prompt_template.replace('{text}', text[:5000])
            prompt = prompt.replace('{chapter}', chapter)
            prompt = prompt.replace('{difficulty}', difficulty)
            
            print(f"\n[LLM CALL] Sending prompt to LLM...")
            print(f"[LLM CALL] Provider: {self.llm.__class__.__name__}")
            print(f"[LLM CALL] Prompt length: {len(prompt)} characters\n")
            
            response = self.llm.generate_json(prompt)
            
            print(f"[LLM RESPONSE] Received response from LLM")
            print(f"[LLM RESPONSE] Response type: {type(response)}")
            print(f"[LLM RESPONSE] Has 'questions' key: {'questions' in response if response else False}")
            
            if response and 'questions' in response:
                question_count = len(response['questions'])
                print(f"✅ [MCQ EXTRACTION] SUCCESS - Extracted {question_count} MCQs")
                print(f"[MCQ EXTRACTION] Questions: {[q.get('question', '')[:50] + '...' for q in response['questions'][:3]]}")
                return response['questions']
            else:
                print(f"❌ [MCQ EXTRACTION] FAILED - LLM did not return questions array")
                logger.warning("LLM did not return questions array")
                return []
        
        except Exception as e:
            logger.error(f"Error extracting MCQs: {e}")
            return []
    
    def _convert_answer_to_int(self, answer: str) -> int:
        """Convert answer letter to integer"""
        answer_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5,
                      'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        try:
            if answer in answer_map:
                return answer_map[answer]
            return int(answer)
        except:
            return 1
