"""
Content Analyzer Module
Detects whether PDF content contains questions/answers or is purely descriptive
"""

import re
import logging

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Analyzes PDF content to determine its type (MCQ vs Descriptive)"""
    
    # Patterns that indicate MCQ content
    MCQ_PATTERNS = [
        r'\bQ\d+\b',  # Q1, Q2, etc.
        r'Q\s*\d+\s*[):\.]',  # Q 1), Q 1:, Q 1.
        r'\bQuestion\s+\d+\b',  # Question 1
        r'\b(?:Ans|Answer|Ans\.)\s*\d*\s*[):\.]',  # Ans:, Ans 1), Answer:
        r'\b(?:Opt|Option|Choices?)\s*[):\.]',  # Option:, Options:
        r'\b(?:A\)|B\)|C\)|D\))',  # A), B), C), D)
        r'\b(?:A\s{0,2}\)|B\s{0,2}\)|C\s{0,2}\)|D\s{0,2}\))',  # A ), B ), etc.
        r'(?:^|\n)\s*(?:A|B|C|D|E)\s*[):-]',  # Lines starting with A), B), C), D), E)
        r'\(a\)|\(b\)|\(c\)|\(d\)',  # (a), (b), (c), (d)
    ]
    
    @staticmethod
    def detect_content_type(content: str) -> str:
        """
        Detect if content contains MCQ structure or is purely descriptive
        
        Args:
            content: Text content from PDF
            
        Returns:
            'mcq' if MCQ structure detected, 'descriptive' if purely descriptive
        """
        if not content or len(content.strip()) < 100:
            return 'descriptive'  # Too short to be reliable
        
        # Count MCQ pattern matches
        pattern_matches = 0
        for pattern in ContentAnalyzer.MCQ_PATTERNS:
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            pattern_matches += len(matches)
        
        # If we found significant MCQ patterns, it's MCQ content
        # Threshold: at least 3 pattern matches or 5% of total lines matching
        lines = content.split('\n')
        if pattern_matches >= 3:
            logger.info(f"MCQ content detected ({pattern_matches} patterns found)")
            return 'mcq'
        
        # If less than 3 patterns, check for high proportion of Q/A patterns
        qa_line_count = 0
        for line in lines:
            if re.search(r'\b(?:Q\d+|Question|Ans|Option)\b|[A-E]\)', line, re.IGNORECASE):
                qa_line_count += 1
        
        qa_proportion = qa_line_count / len(lines) if lines else 0
        if qa_proportion > 0.1:  # If > 10% of lines have QA patterns
            logger.info(f"MCQ content detected ({qa_proportion:.1%} lines with QA patterns)")
            return 'mcq'
        
        logger.info("Descriptive content detected")
        return 'descriptive'
    
    @staticmethod
    def has_options_in_content(content: str) -> bool:
        """
        Check if content contains option markers (A), (B), (C), (D), (E) or similar
        
        Args:
            content: Text content from PDF
            
        Returns:
            True if options are present, False otherwise
        """
        # Check for option patterns
        option_patterns = [
            r'(?:^|\n)\s*(?:A|B|C|D|E)\s*[):\.]',  # A), A:, A.
            r'(?:^|\n)\s*(?:A|B|C|D|E)\s*-\s*',  # A - 
            r'\(A\)|\(B\)|\(C\)|\(D\)|\(E\)',  # (A), (B), etc - fixed escaping
        ]
        
        option_count = 0
        for pattern in option_patterns:
            try:
                matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                option_count += len(matches)
            except re.error as e:
                # Skip invalid patterns
                continue
        
        # If we found multiple option patterns, options likely exist
        return option_count >= 4  # At least 4 option markers
    
    @staticmethod
    def extract_questions_from_content(content: str) -> list:
        """
        Try to extract questions and answers from content
        This is a basic extraction - actual structure depends on PDF format
        
        Args:
            content: Text content from PDF
            
        Returns:
            List of extracted question blocks (or empty list if extraction fails)
        """
        questions = []
        
        # Split by common question markers
        # This is a simplified extraction
        patterns = [
            r'Q\s*(\d+)\s*[):.]\s*(.*?)(?=Q\s*\d+\s*[):.}|$)',  # Q1: ... Q2:
            r'Question\s*(\d+)\s*[):.]\s*(.*?)(?=Question\s*\d+\s*[):.}|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                questions.extend(matches)
        
        return questions[:20]  # Return first 20 extracted questions
