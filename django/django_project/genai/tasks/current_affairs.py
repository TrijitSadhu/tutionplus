"""
Current Affairs Task Module
Scrapes current affairs from websites and uses LLM to generate MCQs and descriptive content
"""

import logging
import requests
from typing import List, Dict, Any, Tuple, Optional
from bs4 import BeautifulSoup
from datetime import datetime, date
import json

from genai.utils.llm_provider import default_llm
from genai.config import CURRENT_AFFAIRS_SOURCES, REQUEST_HEADERS, MAX_RETRIES, RETRY_DELAY
from bank.models import current_affairs  # Adjust based on your MCQ model

logger = logging.getLogger(__name__)


class CurrentAffairsScraper:
    """Scrapes current affairs from websites"""
    
    def __init__(self):
        self.headers = REQUEST_HEADERS
        self.max_retries = MAX_RETRIES
        self.retry_delay = RETRY_DELAY
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a webpage with retry logic
        
        Args:
            url: The URL to fetch
        
        Returns:
            HTML content or None
        """
        import time
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return None
    
    def extract_content(self, html: str, extraction_rules: Dict = None) -> List[Dict[str, str]]:
        """
        Extract current affairs content from HTML
        
        Args:
            html: HTML content
            extraction_rules: CSS selectors or XPath rules for extraction
        
        Returns:
            List of extracted content dictionaries
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            content = []
            
            # Default extraction - modify based on your site structure
            articles = soup.find_all('article') or soup.find_all('div', class_='article')
            
            for article in articles:
                title = article.find('h2', 'h3')
                body = article.find('p', 'div', class_='content')
                
                if title and body:
                    content.append({
                        'title': title.get_text(strip=True),
                        'body': body.get_text(strip=True),
                        'source_url': None
                    })
            
            return content
        
        except Exception as e:
            logger.error(f"Error extracting content from HTML: {str(e)}")
            return []
    
    def scrape_from_sources(self, content_type: str = 'mcq') -> List[Dict[str, Any]]:
        """
        Scrape current affairs from all configured sources
        
        Args:
            content_type: 'mcq' or 'descriptive'
        
        Returns:
            List of scraped content
        """
        sources = CURRENT_AFFAIRS_SOURCES.get(content_type, [])
        all_content = []
        
        for source_url in sources:
            logger.info(f"Scraping {content_type} from {source_url}")
            html = self.fetch_page(source_url)
            
            if html:
                content = self.extract_content(html)
                all_content.extend(content)
        
        return all_content


class CurrentAffairsProcessor:
    """Processes current affairs content with LLM"""
    
    def __init__(self):
        self.llm = default_llm
        self.scraper = CurrentAffairsScraper()
    
    def generate_mcq_prompt(self, title: str, body: str) -> str:
        """Generate a prompt for MCQ creation"""
        return f"""
You are an expert in creating multiple choice questions for competitive exams.
Based on the following current affairs article, generate 3 high-quality MCQ questions.

Title: {title}
Content: {body}

Return ONLY a JSON object with this structure:
{{
    "questions": [
        {{
            "question": "Question text",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "explanation": "Why this answer is correct"
        }}
    ]
}}
"""
    
    def generate_descriptive_prompt(self, title: str, body: str) -> str:
        """Generate a prompt for descriptive content"""
        return f"""
You are an expert in summarizing current affairs for educational purposes.
Summarize the following article in a clear, structured way suitable for study notes.

Title: {title}
Content: {body}

Return ONLY a JSON object with this structure:
{{
    "title": "Article Title",
    "summary": "Detailed summary",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "importance": "Why this is important for competitive exams"
}}
"""
    
    def process_mcq_content(self, title: str, body: str) -> Dict[str, Any]:
        """
        Process current affairs and generate MCQs
        
        Args:
            title: Article title
            body: Article content
        
        Returns:
            Generated MCQs data
        """
        try:
            prompt = self.generate_mcq_prompt(title, body)
            response = self.llm.generate_json(prompt)
            return response
        
        except Exception as e:
            logger.error(f"Error processing MCQ content: {str(e)}")
            return {"error": str(e)}
    
    def process_descriptive_content(self, title: str, body: str) -> Dict[str, Any]:
        """
        Process current affairs for descriptive content
        
        Args:
            title: Article title
            body: Article content
        
        Returns:
            Generated descriptive data
        """
        try:
            prompt = self.generate_descriptive_prompt(title, body)
            response = self.llm.generate_json(prompt)
            return response
        
        except Exception as e:
            logger.error(f"Error processing descriptive content: {str(e)}")
            return {"error": str(e)}
    
    def save_mcq_to_database(self, mcq_data: Dict[str, Any]) -> List[Dict]:
        """
        Save generated MCQs to database
        
        Args:
            mcq_data: MCQ data from LLM
        
        Returns:
            List of saved MCQ IDs
        """
        saved_mcqs = []
        
        try:
            for question_data in mcq_data.get('questions', []):
                # Create MCQ object - adjust model fields based on your schema
                mcq = current_affairs.objects.create(
                    upper_heading=question_data.get('question', ''),
                    yellow_heading=question_data.get('explanation', ''),
                    key_1=question_data.get('option_a', ''),
                    key_2=question_data.get('option_b', ''),
                    key_3=question_data.get('option_c', ''),
                    key_4=question_data.get('option_d', ''),
                    day=date.today(),
                    creation_time=datetime.now().time()
                )
                saved_mcqs.append({'id': mcq.id, 'question': mcq.upper_heading})
                logger.info(f"Saved MCQ: {mcq.id}")
        
        except Exception as e:
            logger.error(f"Error saving MCQ to database: {str(e)}")
        
        return saved_mcqs
    
    def run_complete_pipeline(self, content_type: str = 'mcq') -> Dict[str, Any]:
        """
        Run the complete pipeline: scrape -> process -> save
        
        Args:
            content_type: 'mcq' or 'descriptive'
        
        Returns:
            Results dictionary
        """
        logger.info(f"Starting Current Affairs pipeline for {content_type}")
        
        # Step 1: Scrape
        content_list = self.scraper.scrape_from_sources(content_type)
        logger.info(f"Scraped {len(content_list)} articles")
        
        results = {
            'content_type': content_type,
            'articles_scraped': len(content_list),
            'processed_items': [],
            'errors': []
        }
        
        # Step 2: Process and Save
        for content in content_list:
            try:
                if content_type == 'mcq':
                    processed = self.process_mcq_content(content['title'], content['body'])
                    if 'questions' in processed:
                        saved = self.save_mcq_to_database(processed)
                        results['processed_items'].extend(saved)
                else:
                    processed = self.process_descriptive_content(content['title'], content['body'])
                    results['processed_items'].append(processed)
            
            except Exception as e:
                logger.error(f"Error processing content: {str(e)}")
                results['errors'].append(str(e))
        
        logger.info(f"Pipeline completed. Processed {len(results['processed_items'])} items")
        return results


# Utility functions
def fetch_and_process_current_affairs(content_type: str = 'mcq') -> Dict[str, Any]:
    """
    Convenience function to fetch and process current affairs
    
    Args:
        content_type: 'mcq' or 'descriptive'
    
    Returns:
        Processing results
    """
    processor = CurrentAffairsProcessor()
    return processor.run_complete_pipeline(content_type)
