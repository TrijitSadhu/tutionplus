"""
PDF Processing Task Module
Processes PDF files and generates MCQs for specific chapters and topics
"""

import logging
import os
from typing import List, Dict, Any, Optional
import json
from pathlib import Path

from genai.utils.llm_provider import default_llm
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
                    end = end_page or len(pdf.pages)
                    for i in range(start_page, min(end + 1, len(pdf.pages))):
                        text += pdf.pages[i].extract_text() or ""
                return text
            
            elif PYPDF2_AVAILABLE:
                text = ""
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    end = end_page or len(pdf_reader.pages)
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
    
    def generate_mcq_prompt(self, chapter: str, topic: str, content: str, num_questions: int = 5) -> str:
        """Generate prompt for subject MCQ creation"""
        return f"""
You are an expert educational content creator specializing in {chapter}.
Generate {num_questions} high-quality multiple choice questions aligned with competitive exam standards.

Chapter: {chapter}
Topic: {topic}
Content: {content[:2000]}  # First 2000 chars to save tokens

Create questions that test understanding, not just memorization.

Return ONLY a JSON object with this structure:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "explanation": "Detailed explanation",
            "difficulty": "Easy|Medium|Hard"
        }}
    ]
}}
"""
    
    def process_pdf_for_subject(self, pdf_path: str, chapter: str, topic: str, 
                               start_page: int = 0, end_page: int = None, 
                               num_questions: int = 5) -> Dict[str, Any]:
        """
        Process PDF and generate MCQs for specific chapter/topic
        
        Args:
            pdf_path: Path to PDF file
            chapter: Chapter/Subject name
            topic: Topic name
            start_page: Starting page
            end_page: Ending page
            num_questions: Number of questions to generate
        
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
            
            # Generate MCQs
            logger.info(f"Generating MCQs for {chapter} - {topic}")
            prompt = self.generate_mcq_prompt(chapter, topic, content, num_questions)
            response = self.llm.generate_json(prompt)
            
            return response
        
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            return {"error": str(e)}
    
    def save_mcqs_to_subject_table(self, mcq_data: Dict[str, Any]) -> List[Dict]:
        """
        Save generated MCQs to subject table
        Note: Adjust based on your actual subject model
        
        Args:
            mcq_data: MCQ data from LLM
        
        Returns:
            List of saved item IDs
        """
        saved_items = []
        
        try:
            # Import your subject model
            from bank.models import total  # Adjust based on your model
            
            for question_data in mcq_data.get('questions', []):
                item = total.objects.create(
                    subtopic=mcq_data.get('topic', ''),
                    subtopic_more=question_data.get('question', ''),
                    # Add more fields based on your model
                )
                saved_items.append({'id': item.id})
                logger.info(f"Saved subject MCQ: {item.id}")
        
        except Exception as e:
            logger.error(f"Error saving to subject table: {str(e)}")
        
        return saved_items


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
