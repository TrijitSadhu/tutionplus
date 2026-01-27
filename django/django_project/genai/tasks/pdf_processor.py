"""
PDF Processing Task Module
Processes PDF files and generates MCQs for specific chapters and topics
Supports dual-mode MCQ generation: Descriptive to MCQ and MCQ to MCQ
"""

import logging
import os
from typing import List, Dict, Any, Optional
import json
from pathlib import Path

from genai.utils.llm_provider import default_llm
from genai.utils.content_analyzer import ContentAnalyzer
from genai.config import PDF_UPLOAD_PATH, MAX_PDF_SIZE

logger = logging.getLogger(__name__)

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    logger.warning("PyPDF2 not installed. PDF processing will be limited.")

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    logger.warning("pdfplumber not installed. PDF extraction may be limited.")


class PDFProcessor:
    """Processes PDF files and extracts text"""
    
    def __init__(self):
        self.upload_path = PDF_UPLOAD_PATH
        os.makedirs(self.upload_path, exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Extracted text content
        """
        try:
            text = ""
            
            # Try pdfplumber first (better for complex PDFs)
            if PDFPLUMBER_AVAILABLE:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                return text
            
            # Fallback to PyPDF2
            elif PYPDF2_AVAILABLE:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                return text
            
            else:
                logger.error("No PDF library available")
                return ""
        
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def extract_by_page_range(self, pdf_path: str, start_page: int = 0, end_page: int = None) -> str:
        """
        Extract text from specific page range
        
        Args:
            pdf_path: Path to PDF file
            start_page: Starting page number (0-indexed)
            end_page: Ending page number (inclusive)
        
        Returns:
            Extracted text from specified pages
        """
        try:
            if PDFPLUMBER_AVAILABLE:
                text = ""
                with pdfplumber.open(pdf_path) as pdf:
                    end = end_page if end_page is not None else len(pdf.pages) - 1
                    for i in range(start_page, min(end + 1, len(pdf.pages))):
                        text += pdf.pages[i].extract_text() or ""
                return text
            
            elif PYPDF2_AVAILABLE:
                text = ""
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    end = end_page if end_page is not None else len(pdf_reader.pages) - 1
                    for i in range(start_page, min(end + 1, len(pdf_reader.pages))):
                        text += pdf_reader.pages[i].extract_text()
                return text
        
        except Exception as e:
            logger.error(f"Error extracting page range: {str(e)}")
            return ""
    
    def validate_pdf(self, file_path: str) -> bool:
        """Validate PDF file"""
        if not os.path.exists(file_path):
            logger.error(f"PDF file not found: {file_path}")
            return False
        
        file_size = os.path.getsize(file_path)
        if file_size > MAX_PDF_SIZE:
            logger.error(f"PDF file too large: {file_size} > {MAX_PDF_SIZE}")
            return False
        
        return True


class SubjectMCQGenerator:
    """Generates MCQs from subject PDFs"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.llm = default_llm
    
    def generate_mcq_prompt(self, chapter: str, topic: str, content: str, num_questions: int = 5, difficulty: str = None) -> str:
        """Generate prompt for subject MCQ creation"""
        difficulty_desc = ""
        if difficulty:
            difficulty_map = {
                'easy': 'Easy (suitable for beginners)',
                'medium': 'Medium (balanced difficulty)',
                'hard': 'Hard (challenging, for advanced learners)'
            }
            difficulty_desc = f"\nDifficulty Level: {difficulty_map.get(difficulty, difficulty)}"
        
        # Handle "extract all" marker (999999)
        if num_questions == 999999:
            questions_instruction = "Extract ALL multiple choice questions"
        else:
            questions_instruction = f"Generate {num_questions} high-quality multiple choice questions"
        
        return f"""You are an expert educational content creator specializing in {chapter}.
{questions_instruction} aligned with competitive exam standards.{difficulty_desc}

Chapter: {chapter}
Topic: {topic}
Content: {content[:2000]}

Create questions that test understanding, not just memorization.

Return ONLY a valid JSON object (no markdown, no explanations) with this exact structure:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text here",
            "option_1": "First option",
            "option_2": "Second option", 
            "option_3": "Third option",
            "option_4": "Fourth option",
            "correct_answer": 1,
            "explanation": "Explanation of the correct answer",
            "difficulty": "{difficulty or 'medium'}"
        }}
    ]
}}
"""
    
    def process_pdf_for_subject(self, pdf_path: str, chapter: str, topic: str, 
                               start_page: int = 0, end_page: int = None, 
                               num_questions: int = 5, difficulty: str = None,
                               output_format: str = 'json', subject: str = None,
                               task_type: str = 'pdf_to_mcq') -> Dict[str, Any]:
        """
        Process PDF and generate MCQs for specific chapter/topic
        
        Args:
            pdf_path: Path to PDF file
            chapter: Chapter/Subject name
            topic: Topic name
            start_page: Starting page
            end_page: Ending page
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            output_format: Output format (json, list, etc.)
            subject: Subject name for fetching prompt from database
            task_type: Task type (pdf_to_mcq, pdf_to_descriptive, etc.)
        
        Returns:
            Generated MCQs data
        """
        try:
            # Validate PDF
            if not self.pdf_processor.validate_pdf(pdf_path):
                return {"error": "Invalid PDF file"}
            
            # Extract text
            logger.info(f"Extracting text from {pdf_path}")
            content = self.pdf_processor.extract_by_page_range(pdf_path, start_page, end_page)
            
            if not content:
                return {"error": "No content extracted from PDF"}
            
            # Print page range information
            print(f"\n{'='*80}")
            print(f"[PDF PAGE RANGE]")
            print(f"{'='*80}")
            print(f"Start Page: {start_page}")
            print(f"End Page: {end_page if end_page else 'All remaining pages'}")
            print(f"Content Extracted: {len(content)} characters")
            print(f"{'='*80}\n")
            
            # DUAL-MODE DETECTION: Check if content is MCQ-based or descriptive
            # This is crucial for determining how to process the PDF
            content_type = ContentAnalyzer.detect_content_type(content)
            has_options = ContentAnalyzer.has_options_in_content(content)
            
            print(f"\n{'='*80}")
            print(f"[CONTENT ANALYSIS]")
            print(f"{'='*80}")
            print(f"Content Type Detected: {content_type.upper()}")
            print(f"Has Options in Content: {has_options}")
            if content_type == 'mcq':
                print(f"MODE: MCQ to MCQ (Extract existing Q&A, optionally create/modify options)")
            else:
                print(f"MODE: Descriptive to MCQ (Create Q&A&Options from scratch)")
            print(f"{'='*80}\n")
            
            # Generate MCQs
            logger.info(f"Generating MCQs for {chapter} - {topic}")
            logger.info(f"Content Type: {content_type}, Has Options: {has_options}")
            
            # Determine prompt type based on task_type
            if 'descriptive' in task_type.lower():
                prompt_type = 'descriptive'
            else:
                prompt_type = 'mcq'
            
            # Fetch prompt from database if subject provided, otherwise use hardcoded prompt
            if subject:
                from .task_router import get_llm_prompt_for_task
                prompt_text = get_llm_prompt_for_task(task_type, subject, prompt_type)
                if not prompt_text:
                    logger.warning(f"No {prompt_type} prompt found for {subject}, using default prompt")
                    prompt = self.generate_mcq_prompt(chapter, topic, content, num_questions, difficulty)
                else:
                    # Convert 999999 marker to "ALL" for the LLM
                    num_questions_for_prompt = "ALL" if num_questions == 999999 else num_questions
                    
                    # Use database prompt with safe string substitution (not .format() which breaks with JSON braces)
                    # Include content_type and options_available information for dual-mode support
                    prompt = prompt_text
                    
                    # Safe replacement using string.replace() instead of .format()
                    # This avoids issues with JSON braces in the template
                    replacements = {
                        '{chapter}': str(chapter or ''),
                        '{topic}': str(topic or ''),
                        '{content}': str(content[:3000] if content else ''),
                        '{num_questions}': str(num_questions_for_prompt),
                        '{difficulty}': str(difficulty or 'medium'),
                        '{content_type}': str(content_type or 'mcq'),
                        '{options_available}': str(has_options),
                    }
                    
                    for placeholder, value in replacements.items():
                        prompt = prompt.replace(placeholder, value)
            else:
                prompt = self.generate_mcq_prompt(chapter, topic, content, num_questions, difficulty)
            
            # Print LLM input
            print(f"\n{'='*80}")
            print(f"[LLM INPUT] Sending prompt to LLM")
            print(f"{'='*80}")
            print(f"Prompt Type: {prompt_type}")
            print(f"Task Type: {task_type}")
            print(f"Subject: {subject}")
            print(f"Content Type: {content_type.upper()}")
            print(f"Options Available: {has_options}")
            print(f"Difficulty: {difficulty or 'medium'}")
            if num_questions == 999999:
                print(f"Mode: EXTRACT ALL MCQs from PDF")
            else:
                print(f"Num Questions Requested: {num_questions}")
            print(f"Prompt Length: {len(prompt)} characters")
            print(f"{'-'*80}")
            print(f"PROMPT:\n{prompt[:500]}...\n" if len(prompt) > 500 else f"PROMPT:\n{prompt}\n")
            print(f"{'='*80}\n")
            
            response = self.llm.generate_json(prompt)
            
            # Print LLM output
            print(f"\n{'='*80}")
            print(f"[LLM OUTPUT] Received response from LLM")
            print(f"{'='*80}")
            if response:
                if isinstance(response, dict):
                    questions_count = len(response.get('questions', []))
                    print(f"Response Type: {type(response).__name__}")
                    print(f"Questions Generated: {questions_count}")
                    print(f"Response Keys: {list(response.keys())}")
                    print(f"{'-'*80}")
                    print(f"RESPONSE (First 500 chars):\n{str(response)[:500]}...\n" if len(str(response)) > 500 else f"RESPONSE:\n{response}\n")
                else:
                    print(f"Response Type: {type(response).__name__}")
                    print(f"RESPONSE: {response}\n")
            else:
                print(f"Response: Empty or None\n")
            print(f"{'='*80}\n")
            
            # Check if response is valid and has questions
            if not response:
                logger.error("Empty response from LLM")
                print(f"  ❌ ERROR: LLM returned empty response")
                return {"error": "LLM returned empty response", "questions": []}
            
            if not isinstance(response, dict):
                logger.error(f"Invalid response type: {type(response)}")
                return {"error": "Invalid response format", "questions": []}
            
            if 'questions' not in response or not response.get('questions'):
                logger.warning(f"No questions in response: {response}")
                print(f"  ⚠️  WARNING: No questions generated by LLM")
                return {"error": "No questions generated", "questions": []}
            
            logger.info(f"Successfully generated {len(response.get('questions', []))} MCQs")
            return response
        
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            return {"error": str(e)}
    
    def save_mcqs_to_subject_table(self, mcq_data: Dict[str, Any], subject: str = None, created_by = None, chapter: str = None, difficulty: str = None) -> List[Dict]:
        """
        Save generated MCQs to subject-specific table
        
        Args:
            mcq_data: MCQ data from LLM
            subject: Subject name (e.g., 'polity', 'economics', 'history')
            created_by: User who created this
            chapter: Chapter number (overrides LLM response)
            difficulty: Difficulty level (overrides LLM response)
        
        Returns:
            List of saved item IDs
        """
        saved_items = []
        
        try:
            # Get the appropriate subject model based on subject name
            subject_table = self._get_subject_model(subject)
            if not subject_table:
                logger.error(f"No model found for subject: {subject}")
                return saved_items
            
            for question_data in mcq_data.get('questions', []):
                try:
                    # Create MCQ record with all available fields
                    # Handle different option field names
                    # Get options dict and handle both lowercase and uppercase keys
                    options_dict = question_data.get('options', {})
                    
                    item_data = {
                        'question': question_data.get('question', ''),
                        'option_1': (question_data.get('option_1', '') or 
                                    question_data.get('option_a', '') or 
                                    options_dict.get('A', '') or 
                                    options_dict.get('a', '')),
                        'option_2': (question_data.get('option_2', '') or 
                                    question_data.get('option_b', '') or 
                                    options_dict.get('B', '') or 
                                    options_dict.get('b', '')),
                        'option_3': (question_data.get('option_3', '') or 
                                    question_data.get('option_c', '') or 
                                    options_dict.get('C', '') or 
                                    options_dict.get('c', '')),
                        'option_4': (question_data.get('option_4', '') or 
                                    question_data.get('option_d', '') or 
                                    options_dict.get('D', '') or 
                                    options_dict.get('d', '')),
                    }
                    
                    # Also capture option_5 if available
                    option_5 = (question_data.get('option_5', '') or 
                               question_data.get('option_e', '') or 
                               options_dict.get('E', '') or 
                               options_dict.get('e', ''))
                    if option_5:
                        item_data['option_5'] = option_5
                    
                    # Handle answer field - accepts various formats
                    answer = (question_data.get('correct_answer') or 
                             question_data.get('answer') or 
                             question_data.get('ans'))
                    
                    if answer:
                        # Convert various formats to number
                        if isinstance(answer, str):
                            if answer.upper() in ['A', 'B', 'C', 'D', 'E']:
                                answer = ord(answer.upper()) - ord('A') + 1
                            elif answer.lower() in ['a', 'b', 'c', 'd', 'e']:
                                answer = ord(answer.lower()) - ord('a') + 1
                            else:
                                try:
                                    answer = int(answer)
                                except (ValueError, TypeError):
                                    answer = None
                        
                        if answer:
                            item_data['ans'] = int(answer)
                    
                    # Add optional fields
                    # Use passed-in values (from form) if available, otherwise fall back to LLM response
                    if chapter:
                        item_data['chapter'] = chapter
                    elif 'chapter' in question_data:
                        item_data['chapter'] = question_data.get('chapter')
                    
                    if difficulty:
                        item_data['difficulty'] = difficulty
                    elif 'difficulty' in question_data:
                        item_data['difficulty'] = question_data.get('difficulty')
                    
                    if 'explanation' in question_data:
                        item_data['extra'] = question_data.get('explanation')  # Map explanation to 'extra' field
                    
                    # Add created_by only if the model has this field
                    if created_by:
                        # Check if the model has a created_by field
                        if hasattr(subject_table, '_meta'):
                            field_names = [f.name for f in subject_table._meta.get_fields()]
                            if 'created_by' in field_names:
                                item_data['created_by'] = created_by
                    
                    # Create the record
                    item = subject_table.objects.create(**item_data)
                    saved_items.append({'id': item.id})
                    logger.info(f"Saved {subject} MCQ: {item.id}")
                    print(f"    ✓ Saved question {len(saved_items)}")
                
                except Exception as e:
                    logger.error(f"Error saving individual MCQ: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error saving to subject table: {str(e)}")
        
        return saved_items
    
    def _get_subject_model(self, subject: str):
        """Get the appropriate Django model for the subject"""
        if not subject:
            return None
        
        subject_lower = subject.lower().replace(' ', '_')
        
        try:
            from django.apps import apps
            
            # Try common naming conventions for subject-specific tables
            # Priority order: polity, chemistry, history, geography, etc.
            model_names = [
                subject_lower,  # polity (direct match)
                f"{subject_lower}s",  # polities (plural)
                f"{subject_lower}_mcq",  # polity_mcq
                f"total_{subject_lower}",  # total_polity (fallback)
            ]
            
            for model_name in model_names:
                try:
                    # Try to get from bank app first
                    model = apps.get_model('bank', model_name)
                    logger.info(f"Using model 'bank.{model_name}' for subject: {subject}")
                    print(f"  ✓ Using model: bank.{model_name}")
                    return model
                except LookupError:
                    try:
                        # Try genai app
                        model = apps.get_model('genai', model_name)
                        logger.info(f"Using model 'genai.{model_name}' for subject: {subject}")
                        print(f"  ✓ Using model: genai.{model_name}")
                        return model
                    except LookupError:
                        continue
            
            # Fallback to generic MCQ tables if subject-specific table not found
            fallback_models = ['total_mcq', 'total']
            for fallback_model in fallback_models:
                try:
                    model = apps.get_model('bank', fallback_model)
                    logger.warning(f"Subject-specific model not found for '{subject}', using fallback: {fallback_model}")
                    print(f"  ⚠️  Subject-specific model not found for '{subject}', using fallback: bank.{fallback_model}")
                    return model
                except LookupError:
                    continue
            
            logger.error(f"No model found for subject: {subject}")
            print(f"  ❌ ERROR: No model found for subject: {subject}")
            return None
        
        except Exception as e:
            logger.error(f"Error getting subject model: {str(e)}")
            return None


# ======================= CURRENT AFFAIRS PROCESSORS =======================

class CurrentAffairsProcessor(SubjectMCQGenerator):
    """Process PDFs for Current Affairs MCQ and Descriptive content"""
    
    def process_currentaffairs_mcq(self, pdf_path: str, num_questions: int = 5, 
                                    start_page: int = 0, end_page: int = None) -> Dict[str, Any]:
        """
        Process PDF for Current Affairs MCQ generation
        
        Args:
            pdf_path: Path to PDF file
            num_questions: Number of MCQs to generate
            start_page: Starting page (0-indexed)
            end_page: Ending page (inclusive)
        
        Returns:
            Dictionary with questions and metadata
        """
        try:
            # Extract PDF content
            if not self.pdf_processor.validate_pdf(pdf_path):
                return {"error": "Invalid PDF file", "questions": []}
            
            content = self.pdf_processor.extract_by_page_range(pdf_path, start_page, end_page)
            
            if not content:
                return {"error": "No content extracted from PDF", "questions": []}
            
            # Get Current Affairs MCQ prompt
            from genai.tasks.task_router import get_llm_prompt_for_task
            prompt_text = get_llm_prompt_for_task('pdf_currentaffairs_mcq', 'current_affairs', 'mcq')
            
            if not prompt_text:
                logger.warning("No CA MCQ prompt found, using default")
                # Use a default prompt for CA MCQ
                prompt_text = self._get_default_ca_mcq_prompt()
            
            # Replace placeholders
            prompt = prompt_text
            replacements = {
                '{title}': 'Current Affairs Article',
                '{content}': content[:3000],
                '{num_questions}': str(num_questions),
            }
            
            for placeholder, value in replacements.items():
                prompt = prompt.replace(placeholder, value)
            
            print(f"\n{'='*80}")
            print(f"[CA MCQ LLM INPUT]")
            print(f"{'='*80}")
            print(f"Prompt Length: {len(prompt)} chars\n")
            
            # Call LLM
            response = self.llm.generate_json(prompt)
            
            print(f"\n{'='*80}")
            print(f"[CA MCQ RESPONSE]")
            print(f"{'='*80}")
            if response and 'questions' in response:
                print(f"Questions generated: {len(response.get('questions', []))}\n")
            else:
                print(f"No questions in response\n")
            
            return response if response else {"questions": []}
        
        except Exception as e:
            logger.error(f"Error processing CA MCQ: {str(e)}")
            return {"error": str(e), "questions": []}
    
    def process_currentaffairs_descriptive(self, pdf_path: str, 
                                           start_page: int = 0, end_page: int = None) -> Dict[str, Any]:
        """
        Process PDF for Current Affairs Descriptive content
        
        Args:
            pdf_path: Path to PDF file
            start_page: Starting page (0-indexed)
            end_page: Ending page (inclusive)
        
        Returns:
            Dictionary with descriptive content
        """
        try:
            # Extract PDF content
            if not self.pdf_processor.validate_pdf(pdf_path):
                return {"error": "Invalid PDF file"}
            
            content = self.pdf_processor.extract_by_page_range(pdf_path, start_page, end_page)
            
            if not content:
                return {"error": "No content extracted from PDF"}
            
            # Get Current Affairs Descriptive prompt
            from genai.tasks.task_router import get_llm_prompt_for_task
            prompt_text = get_llm_prompt_for_task('pdf_currentaffairs_descriptive', 'current_affairs', 'descriptive')
            
            if not prompt_text:
                logger.warning("No CA Descriptive prompt found, using default")
                prompt_text = self._get_default_ca_descriptive_prompt()
            
            # Replace placeholders
            prompt = prompt_text
            replacements = {
                '{title}': 'Current Affairs Study Material',
                '{content}': content[:3000],
            }
            
            for placeholder, value in replacements.items():
                prompt = prompt.replace(placeholder, value)
            
            print(f"\n{'='*80}")
            print(f"[CA DESCRIPTIVE LLM INPUT]")
            print(f"{'='*80}")
            print(f"Prompt Length: {len(prompt)} chars\n")
            
            # Call LLM
            response = self.llm.generate_json(prompt)
            
            print(f"\n{'='*80}")
            print(f"[CA DESCRIPTIVE RESPONSE]")
            print(f"{'='*80}")
            if response:
                print(f"Content generated: {bool(response.get('upper_heading'))}\n")
            else:
                print(f"No content in response\n")
            
            return response if response else {}
        
        except Exception as e:
            logger.error(f"Error processing CA Descriptive: {str(e)}")
            return {"error": str(e)}
    
    def _get_default_ca_mcq_prompt(self) -> str:
        """Default Current Affairs MCQ prompt"""
        return """You are an expert in creating multiple choice questions for competitive exams based on current affairs.
Based on the provided current affairs article, generate {num_questions} high-quality MCQ questions.

Title: {title}
Content: {content}

For each question, return in JSON format with categories (array of applicable categories):
{{
    "questions": [
        {{
            "question": "...",
            "option_1": "...",
            "option_2": "...",
            "option_3": "...",
            "option_4": "...",
            "correct_answer": 1,
            "explanation": "...",
            "categories": ["National"]
        }}
    ]
}}"""
    
    def _get_default_ca_descriptive_prompt(self) -> str:
        """Default Current Affairs Descriptive prompt"""
        return """You are an expert in creating current affairs study material for competitive exams.
Based on the provided article, create study material.

Title: {title}
Content: {content}

Provide in JSON format:
{{
    "upper_heading": "Main heading...",
    "yellow_heading": "Key point heading...",
    "key_1": "Key point 1",
    "key_2": "Key point 2",
    "key_3": "Key point 3",
    "key_4": "Key point 4",
    "all_key_points": "Point 1...///Point 2...///Point 3...",
    "categories": ["National", "Business_Economy_Banking"]
}}"""


def process_subject_pdf(pdf_path: str, chapter: str, topic: str, **kwargs) -> Dict[str, Any]:
    """
    Convenience function to process subject PDF
    
    Args:
        pdf_path: Path to PDF file
        chapter: Chapter/Subject name
        topic: Topic name
        **kwargs: Additional arguments
    
    Returns:
        Processing results
    """
    generator = SubjectMCQGenerator()
    return generator.process_pdf_for_subject(pdf_path, chapter, topic, **kwargs)
