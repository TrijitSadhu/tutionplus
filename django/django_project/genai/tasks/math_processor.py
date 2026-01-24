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
