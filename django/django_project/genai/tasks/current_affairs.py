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
from genai.models import LLMPrompt
from bank.models import currentaffairs_descriptive, currentaffairs_mcq

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
    
    def extract_content(self, html: str, source_url: str = None, extraction_rules: Dict = None) -> List[Dict[str, str]]:
        """
        Extract current affairs content from HTML with flexible parsing
        
        Args:
            html: HTML content
            source_url: The URL being scraped (for source-specific prompts)
            extraction_rules: CSS selectors or XPath rules for extraction
        
        Returns:
            List of extracted content dictionaries
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            content = []
            
            print(f"    📊 Parsing HTML structure...")
            
            # Strategy 1: Look for article containers
            articles = soup.find_all('article')
            if not articles:
                articles = soup.find_all('div', class_=lambda x: x and ('article' in x.lower() or 'post' in x.lower() or 'content' in x.lower()))
            
            if not articles:
                # Strategy 2: Look for any divs with substantial text content
                all_divs = soup.find_all('div', class_=lambda x: x and ('item' in x.lower() or 'entry' in x.lower() or 'card' in x.lower()))
                if all_divs:
                    articles = all_divs
            
            print(f"    📊 Found {len(articles)} potential article containers")
            
            for idx, article in enumerate(articles, 1):
                title = None
                body = None
                
                # Try to find title in various heading tags
                for heading_tag in ['h1', 'h2', 'h3', 'h4']:
                    title_elem = article.find(heading_tag)
                    if title_elem and title_elem.get_text(strip=True):
                        title = title_elem.get_text(strip=True)
                        break
                
                # Try to find body/content in various container tags
                for container_tag in ['p', 'div', 'span']:
                    body_elem = article.find(container_tag)
                    if body_elem:
                        body_text = body_elem.get_text(strip=True)
                        if body_text and len(body_text) > 20:  # At least 20 characters
                            body = body_text
                            break
                
                # Extract all text as fallback
                if not body:
                    body = article.get_text(strip=True)
                    # Remove title from body if it's there
                    if title and body.startswith(title):
                        body = body[len(title):].strip()
                
                if title and body and len(body) > 20:
                    content.append({
                        'title': title[:200],  # Limit title length
                        'body': body[:2000],   # Limit body length
                        'source_url': source_url
                    })
                    print(f"      ✓ Article {idx}: Extracted title ({len(title)} chars), body ({len(body)} chars)")
            
            # Fallback: If no articles found, try extracting all substantial text blocks
            if not content:
                print(f"    ℹ️  No article containers found, trying alternative extraction...")
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get all paragraphs
                paragraphs = soup.find_all('p')
                
                # Group consecutive paragraphs as articles
                grouped_content = []
                current_group = []
                
                for para in paragraphs:
                    text = para.get_text(strip=True)
                    if text and len(text) > 10:
                        current_group.append(text)
                    elif current_group:
                        grouped_content.append(current_group)
                        current_group = []
                
                if current_group:
                    grouped_content.append(current_group)
                
                print(f"    ℹ️  Found {len(grouped_content)} text groups")
                
                # Convert groups to content items
                for group in grouped_content[:5]:  # Limit to first 5 groups
                    if group:
                        title = group[0][:200]  # First line as title
                        body = ' '.join(group)[:2000]  # Rest as body
                        
                        if len(title) > 10 and len(body) > 20:
                            content.append({
                                'title': title,
                                'body': body,
                                'source_url': source_url
                            })
                            print(f"      ✓ Extracted from text group: title ({len(title)} chars), body ({len(body)} chars)")
            
            return content
        
        except Exception as e:
            logger.error(f"Error extracting content from HTML: {str(e)}")
            print(f"    ❌ Extraction error: {str(e)}")
            return []
    
    def scrape_from_sources(self, content_type: str = 'currentaffairs_mcq') -> List[Dict[str, Any]]:
        """
        Scrape current affairs from sources (fetches from genai.ContentSource)
        
        Args:
            content_type: 'currentaffairs_mcq' or 'currentaffairs_descriptive'
        
        Returns:
            List of scraped content with source URLs
        """
        print(f"\n📋 [SCRAPER] scrape_from_sources() - Starting scrape for content_type: {content_type}")
        try:
            # Fetch active sources from genai.ContentSource model
            from genai.models import ContentSource
            
            # Map content_type to source_type in ContentSource
            type_mapping = {
                'currentaffairs_mcq': 'currentaffairs_mcq',
                'currentaffairs_descriptive': 'currentaffairs_descriptive'
            }
            source_type = type_mapping.get(content_type, content_type)
            
            # Query active sources from database
            sources = ContentSource.objects.filter(
                is_active=True,
                source_type=source_type
            ).values_list('url', flat=True)
            
            if sources:
                sources = list(sources)
                print(f"  ✓ Found {len(sources)} active sources in ContentSource")
                for src in sources:
                    print(f"    - {src}")
            else:
                # Fallback to hardcoded config if no sources in database
                sources = CURRENT_AFFAIRS_SOURCES.get(content_type, [])
                print(f"  ⚠ No sources in DB, using fallback config with {len(sources)} sources")
                logger.info(f"No active sources in ContentSource, using fallback config: {sources}")
        except Exception as e:
            # If database query fails, use hardcoded config
            print(f"  ❌ Database error: {e}")
            logger.warning(f"Could not fetch from ContentSource: {e}. Using fallback config.")
            sources = CURRENT_AFFAIRS_SOURCES.get(content_type, [])
        
        all_content = []
        
        for idx, source_url in enumerate(sources, 1):
            print(f"\n  🔄 [{idx}/{len(sources)}] Fetching from: {source_url}")
            logger.info(f"Scraping {content_type} from {source_url}")
            html = self.fetch_page(source_url)
            
            if html:
                print(f"    ✓ HTML fetched, extracting content...")
                content = self.extract_content(html, source_url)  # Pass source_url
                print(f"    ✓ Extracted {len(content)} items")
                all_content.extend(content)
            else:
                print(f"    ✗ Failed to fetch HTML")
        
        print(f"\n📋 [SCRAPER] Total content extracted: {len(all_content)} items\n")
        return all_content


class CurrentAffairsProcessor:
    """Processes current affairs content with LLM"""
    
    def __init__(self):
        self.llm = default_llm
        self.scraper = CurrentAffairsScraper()
    
    def get_prompt_from_database(self, prompt_type: str, source_url: str = None) -> str:
        """
        Fetch prompt from database for a given source URL and prompt type.
        Falls back to default prompt if source-specific not found.
        
        Args:
            prompt_type: 'mcq' or 'descriptive'
            source_url: Optional URL to fetch source-specific prompt
        
        Returns:
            Prompt text from database or None if not found
        """
        print(f"  📋 [PROMPT] get_prompt_from_database() - Type: {prompt_type}, Source: {source_url[:50] if source_url else '(None)'}")
        try:
            query = LLMPrompt.objects.filter(
                prompt_type=prompt_type,
                is_active=True
            )
            
            # If source_url provided, prioritize source-specific prompt
            if source_url:
                prompt = query.filter(source_url=source_url, is_default=False).first()
                if prompt:
                    print(f"    ✓ Found SITE-SPECIFIC prompt for {source_url[:50]}")
                    return prompt.prompt_text
                print(f"    ⚠ No site-specific prompt found, trying default...")
            
            # Fall back to default prompt
            prompt = query.filter(is_default=True).first()
            if prompt:
                print(f"    ✓ Using DEFAULT prompt for type '{prompt_type}'")
                return prompt.prompt_text
            
            print(f"    ✗ NO PROMPT FOUND for type '{prompt_type}'")
            return None
        
        except Exception as e:
            print(f"    ❌ ERROR: {str(e)}")
            logger.error(f"Error fetching prompt from database: {str(e)}")
            return None
    
    def generate_mcq_prompt(self, title: str, body: str, source_url: str = None) -> str:
        """Generate a prompt for MCQ creation"""
        print(f"  📋 [PROMPT_GEN] generate_mcq_prompt() - Source: {source_url[:40] if source_url else 'default'}")
        
        # Try to fetch custom prompt from database
        db_prompt = self.get_prompt_from_database('mcq', source_url)
        
        if db_prompt:
            print(f"    ✓ Using DATABASE prompt for MCQ generation")
            # Use database prompt with the current article content
            # Use safe format to avoid KeyError on JSON braces
            try:
                formatted = db_prompt.format(title=title, content=body)
                print(f"    ✓ Prompt formatted successfully (length: {len(formatted)} chars)")
                return formatted
            except (KeyError, ValueError):
                # If format fails, substitute manually
                formatted = db_prompt.replace('{title}', title).replace('{content}', body)
                print(f"    ⚠️  Used manual substitution for prompt (length: {len(formatted)} chars)")
                return formatted
        
        # Fall back to default hardcoded prompt
        print(f"    ✓ Using HARDCODED prompt template for MCQ generation")
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
    
    def generate_descriptive_prompt(self, title: str, body: str, source_url: str = None) -> str:
        """Generate a prompt for descriptive content"""
        print(f"  📋 [PROMPT_GEN] generate_descriptive_prompt() - Source: {source_url[:40] if source_url else 'default'}")
        
        # Try to fetch custom prompt from database
        db_prompt = self.get_prompt_from_database('descriptive', source_url)
        
        if db_prompt:
            print(f"    ✓ Using DATABASE prompt for descriptive generation")
            # Use database prompt with the current article content
            # Use safe format to avoid KeyError on JSON braces
            try:
                formatted = db_prompt.format(title=title, content=body)
                print(f"    ✓ Prompt formatted successfully (length: {len(formatted)} chars)")
                return formatted
            except (KeyError, ValueError):
                # If format fails, substitute manually
                formatted = db_prompt.replace('{title}', title).replace('{content}', body)
                print(f"    ⚠️  Used manual substitution for prompt (length: {len(formatted)} chars)")
                return formatted
        
        # Fall back to default hardcoded prompt
        print(f"    ✓ Using HARDCODED prompt template for descriptive generation")
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
    
    def process_mcq_content(self, title: str, body: str, source_url: str = None) -> Dict[str, Any]:
        """
        Process current affairs and generate MCQs
        
        Args:
            title: Article title
            body: Article content
            source_url: Optional source URL for fetching source-specific prompts
        
        Returns:
            Generated MCQs data
        """
        print(f"  📋 [PROCESSOR] process_mcq_content() - Starting MCQ generation")
        try:
            prompt = self.generate_mcq_prompt(title, body, source_url)
            print(f"    📤 Sending to LLM...")
            response = self.llm.generate_json(prompt)
            print(f"    ✓ LLM response received: {type(response)}")
            return response
        
        except Exception as e:
            print(f"    ❌ ERROR: {str(e)}")
            logger.error(f"Error processing MCQ content: {str(e)}")
            return {"error": str(e)}
    
    def process_descriptive_content(self, title: str, body: str, source_url: str = None) -> Dict[str, Any]:
        """
        Process current affairs for descriptive content
        
        Args:
            title: Article title
            body: Article content
            source_url: Optional source URL for fetching source-specific prompts
        
        Returns:
            Generated descriptive data
        """
        print(f"  📋 [PROCESSOR] process_descriptive_content() - Starting descriptive generation")
        try:
            prompt = self.generate_descriptive_prompt(title, body, source_url)
            print(f"    📤 Sending to LLM...")
            response = self.llm.generate_json(prompt)
            print(f"    ✓ LLM response received: {type(response)}")
            return response
        
        except Exception as e:
            print(f"    ❌ ERROR: {str(e)}")
            logger.error(f"Error processing descriptive content: {str(e)}")
            return {"error": str(e)}
    
    def save_mcq_to_database(self, mcq_data: Dict[str, Any], content_type: str = 'currentaffairs_mcq') -> List[Dict]:
        """
        Save generated MCQs to database
        
        Args:
            mcq_data: MCQ data from LLM
            content_type: 'currentaffairs_mcq' or 'currentaffairs_descriptive'
        
        Returns:
            List of saved MCQ IDs
        """
        print(f"  📋 [SAVER] save_mcq_to_database() - Type: {content_type}")
        saved_mcqs = []
        
        try:
            # Select the appropriate model based on content_type
            if content_type == 'currentaffairs_mcq':
                model = currentaffairs_mcq
            else:
                model = currentaffairs_descriptive
            
            questions = mcq_data.get('questions', [])
            print(f"    📥 Saving {len(questions)} questions...")
            
            for idx, question_data in enumerate(questions, 1):
                # Create MCQ object - adjust model fields based on your schema
                mcq = model.objects.create(
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
                print(f"      [{idx}] ✓ Saved MCQ ID: {mcq.id}")
                logger.info(f"Saved MCQ: {mcq.id}")
        
        except Exception as e:
            print(f"    ❌ ERROR saving to database: {str(e)}")
            logger.error(f"Error saving MCQ to database: {str(e)}")
        
        print(f"    ✓ Total saved: {len(saved_mcqs)} MCQs\n")
        return saved_mcqs
    
    def run_complete_pipeline(self, content_type: str = 'mcq') -> Dict[str, Any]:
        """
        Run the complete pipeline: scrape -> process -> save
        
        Args:
            content_type: 'mcq' or 'descriptive'
        
        Returns:
            Results dictionary
        """
        print(f"\n{'='*70}")
        print(f"🚀 PIPELINE START - Content Type: {content_type}")
        print(f"{'='*70}")
        logger.info(f"Starting Current Affairs pipeline for {content_type}")
        
        # Step 1: Scrape
        print(f"\n[STEP 1] SCRAPING...")
        content_list = self.scraper.scrape_from_sources(content_type)
        print(f"\n✅ [STEP 1] Scraped {len(content_list)} articles")
        logger.info(f"Scraped {len(content_list)} articles")
        
        results = {
            'content_type': content_type,
            'articles_scraped': len(content_list),
            'processed_items': [],
            'errors': []
        }
        
        # Step 2: Process and Save
        print(f"\n[STEP 2] PROCESSING & SAVING...")
        for idx, content in enumerate(content_list, 1):
            print(f"\n  [{idx}/{len(content_list)}] Processing article: {content['title'][:50]}...")
            try:
                source_url = content.get('source_url')
                print(f"    Source URL: {source_url}")
                if content_type == 'currentaffairs_mcq':
                    processed = self.process_mcq_content(content['title'], content['body'], source_url)
                    if 'questions' in processed:
                        saved = self.save_mcq_to_database(processed, content_type)
                        results['processed_items'].extend(saved)
                    else:
                        print(f"    ⚠ No 'questions' key in response")
                else:
                    processed = self.process_descriptive_content(content['title'], content['body'], source_url)
                    results['processed_items'].append(processed)
            
            except Exception as e:
                print(f"    ❌ ERROR: {str(e)}")
                logger.error(f"Error processing content: {str(e)}")
                results['errors'].append(str(e))
        
        print(f"\n{'='*70}")
        print(f"✅ PIPELINE COMPLETE")
        print(f"  Total Processed: {len(results['processed_items'])}")
        print(f"  Errors: {len(results['errors'])}")
        print(f"{'='*70}\n")
        logger.info(f"Pipeline completed. Processed {len(results['processed_items'])} items")
        return results


# Utility functions
def fetch_and_process_current_affairs(content_type: str = 'currentaffairs_mcq') -> Dict[str, Any]:
    """
    Main function to fetch and process current affairs content
    
    Args:
        content_type: 'currentaffairs_mcq' or 'current_affairs_descriptive'
    
    Returns:
        Processing results
    """
    print("\n" + "="*70)
    print(f"🎯 fetch_and_process_current_affairs() CALLED")
    print(f"   Content Type: {content_type}")
    print("="*70)
    
    try:
        print(f"  📍 Initializing CurrentAffairsProcessor...")
        processor = CurrentAffairsProcessor()
        print(f"  ✓ Processor initialized successfully")
        
        print(f"  📞 Calling processor.run_complete_pipeline({content_type})...")
        result = processor.run_complete_pipeline(content_type)
        print(f"  ✅ Pipeline completed, returning result")
        return result
    except Exception as e:
        print(f"  ❌ ERROR in fetch_and_process_current_affairs: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e), 'processed_count': 0}
