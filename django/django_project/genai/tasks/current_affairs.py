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
import time

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logging.warning("Selenium not installed. Install with: pip install selenium webdriver-manager")

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
        self.selenium_available = SELENIUM_AVAILABLE
    
    def fetch_page_selenium(self, url: str) -> Optional[str]:
        """
        Fetch a webpage using Selenium (handles JavaScript-rendered content)
        Uses webdriver-manager for automatic ChromeDriver management
        
        Args:
            url: The URL to fetch
        
        Returns:
            HTML content or None
        """
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available, falling back to requests")
            return None
        
        driver = None
        try:
            # Configure Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument(f'user-agent={self.headers.get("User-Agent", "")}')
            
            print(f"    [SELENIUM] Starting WebDriver for: {url[:50]}...")
            # Use webdriver-manager for automatic driver management
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(url)
            
            # Wait for content to load (up to 10 seconds)
            print(f"    [SELENIUM] Waiting for page to load...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for dynamic content
            time.sleep(3)
            
            html = driver.page_source
            print(f"    [SELENIUM] ✅ Successfully fetched {len(html)} bytes")
            return html
            
        except Exception as e:
            logger.error(f"[SELENIUM] Error fetching {url}: {str(e)}")
            print(f"    [SELENIUM] ❌ Error: {str(e)}")
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a webpage - tries Selenium first, then falls back to requests
        
        Args:
            url: The URL to fetch
        
        Returns:
            HTML content or None
        """
        # Try Selenium first (default choice)
        if SELENIUM_AVAILABLE:
            print(f"    [FETCH] Attempting Selenium (JavaScript support)...")
            html = self.fetch_page_selenium(url)
            if html:
                return html
        
        # Fallback to requests
        print(f"    [FETCH] Falling back to requests...")
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                print(f"    [FETCH] ✅ Requests succeeded ({len(response.text)} bytes)")
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
            
            print(f"    [EXTRACTION] Parsing HTML structure...")
            
            # Strategy 1: Look for quiz questions specifically (wp_quiz_question class)
            quiz_questions = soup.find_all('div', class_='wp_quiz_question')
            if quiz_questions:
                print(f"    [EXTRACTION] Found {len(quiz_questions)} quiz questions (wp_quiz_question)")
                # Extract title from page
                title_elem = soup.find('h1') or soup.find('title')
                page_title = title_elem.get_text(strip=True) if title_elem else "Quiz"
                
                # Combine all quiz questions into one content block
                all_questions = []
                for q in quiz_questions:
                    q_text = q.get_text(strip=True)
                    if q_text:
                        all_questions.append(q_text)
                
                if all_questions:
                    quiz_body = " | ".join(all_questions)
                    content.append({
                        'title': page_title[:200],
                        'body': quiz_body[:2000],
                        'source_url': source_url
                    })
                    print(f"    [EXTRACTION] Extracted quiz content: {len(quiz_body)} chars")
                    return content
            
            # Strategy 1b: Look for IndiaBIX specific content (exam preparation content)
            indiabix_content = soup.find_all(['section', 'div'], class_=lambda x: x and any(keyword in (x.lower() if x else '') for keyword in ['mcq', 'question', 'exam', 'practice', 'quiz', 'topic']))
            if indiabix_content and len(indiabix_content) > 0:
                print(f"    [EXTRACTION] Found {len(indiabix_content)} IndiaBIX content sections")
                title_elem = soup.find('h1') or soup.find('h2') or soup.find('title')
                page_title = title_elem.get_text(strip=True) if title_elem else "Current Affairs"
                
                all_content = []
                for section in indiabix_content[:5]:  # Take first 5 sections
                    section_text = section.get_text(strip=True)
                    if section_text and len(section_text) > 50 and '©' not in section_text and '™' not in section_text:
                        all_content.append(section_text)
                
                if all_content:
                    body = " ".join(all_content)
                    if len(body) > 50:
                        content.append({
                            'title': page_title[:200],
                            'body': body[:2000],
                            'source_url': source_url
                        })
                        print(f"    [EXTRACTION] Extracted IndiaBIX content: {len(body)} chars")
                        return content
            
            # Fallback: Look for article containers
            articles = soup.find_all('article')
            if not articles:
                articles = soup.find_all('div', class_=lambda x: x and ('article' in x.lower() or 'post' in x.lower() or 'content' in x.lower()))
            
            if not articles:
                # Strategy 2: Look for any divs with substantial text content
                all_divs = soup.find_all('div', class_=lambda x: x and ('item' in x.lower() or 'entry' in x.lower() or 'card' in x.lower()))
                if all_divs:
                    articles = all_divs
            
            print(f"    [EXTRACTION] Found {len(articles)} article containers")
            
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
                
                if not body:
                    body = article.get_text(strip=True)
                    # Remove title from body if it's there
                    if title and body.startswith(title):
                        body = body[len(title):].strip()
                    # Skip if body is just copyright/trademark symbols
                    if body and (body == title or len(body) < 50 or '©' in body[:30]):
                        continue
                
                if title and body and len(body) > 50:
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
                extracted_items = self.extract_content(html, source_url)  # Pass source_url
                print(f"    ✓ Extracted {len(extracted_items)} items from URL")
                
                # COMBINE all articles from same URL into ONE content block
                # This ensures 1 URL = 1 LLM call (treating multiple articles as sections)
                if extracted_items:
                    combined_content = {
                        'title': extracted_items[0]['title'],  # Use first article as main heading
                        'body': '\n\n---\n\n'.join([item['body'] for item in extracted_items]),  # Separate articles with delimiter
                        'source_url': source_url
                    }
                    print(f"    ✓ Combined {len(extracted_items)} items into 1 content block for LLM")
                    all_content.append(combined_content)
            else:
                print(f"    ✗ Failed to fetch HTML")
        
        print(f"\n📋 [SCRAPER] Total content items for processing: {len(all_content)} (1 per source URL)\n")
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
    
    def generate_mcq_prompt(self, title: str, body: str, source_url: str = None, skip_scraping: bool = False) -> str:
        """Generate a prompt for MCQ creation"""
        print(f"  📋 [PROMPT_GEN] generate_mcq_prompt() - Source: {source_url[:40] if source_url else 'default'}, SkipMode: {skip_scraping}")
        
        # In skip-scraping mode, try to use the special skip-scraping prompt first
        if skip_scraping:
            print(f"    🔍 [SKIP MODE] Looking for skip-scraping specific prompt")
            db_prompt = self.get_prompt_from_database('mcq', 'skip_scraping_mode')
            if db_prompt:
                print(f"    ✓ Using SKIP-SCRAPING prompt (LLM will fetch URL)")
                try:
                    formatted = db_prompt.format(title=title, content=body)
                    return formatted
                except (KeyError, ValueError):
                    formatted = db_prompt.replace('{title}', title).replace('{content}', body)
                    return formatted
        
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
Based on the following current affairs article, generate 4 high-quality MCQ questions.

Title: {title}
Content: {body}

CATEGORY CLASSIFICATION:
After analyzing the article content, classify which of these categories the MCQ belongs to. 
Select ALL that apply (can be multiple). Use your judgment - if not explicitly mentioned, decide based on content:
- Science_Techonlogy: For technology, innovation, research, engineering
- National: For India-specific news, policies, government, national events
- International: For global news, international relations, foreign countries
- Business_Economy_Banking: For economy, business, markets, finance, banking, commerce
- Environment: For environmental issues, climate, pollution, conservation
- Defence: For military, defence, security, armed forces
- Sports: For sports events, athletes, tournaments
- Art_Culture: For arts, culture, heritage, literature, music
- Awards_Honours: For awards, honors, recognitions, achievements
- Persons_in_News: For notable personalities, appointments, resignations
- Government_Schemes: For government programs, policies, schemes
- State: For state-specific news (if mentioned which state)
- appointment: For appointments, new positions, leadership changes
- obituary: For death announcements, obituaries
- important_day: For special days, commemorations, anniversaries
- rank: For rankings, ratings, positions
- mythology: For historical or mythological references
- agreement: For treaties, agreements, MOUs

For each question, provide:
- question: Clear question text based on the article content
- option_1, option_2, option_3, option_4: Four distinct options
- correct_answer: 1, 2, 3, or 4 (the correct option number)
- explanation: Detailed bullet-point explanation of why this answer is correct. Use bullet points with the format:
  • Key point 1 supporting why this is correct
  • Key point 2 from the article
  • Key point 3 explaining the concept
- categories: Array of category names that apply to this question (e.g., ["National", "Business_Economy_Banking"])

Return ONLY a JSON object with this structure:
{{
    "questions": [
        {{
            "question": "Question text",
            "option_1": "Option 1",
            "option_2": "Option 2",
            "option_3": "Option 3",
            "option_4": "Option 4",
            "correct_answer": 1,
            "explanation": "• Key point 1\\n• Key point 2\\n• Key point 3",
            "categories": ["Category1", "Category2"]
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
    
    def process_mcq_content(self, title: str, body: str, source_url: str = None, skip_scraping: bool = False) -> Dict[str, Any]:
        """
        Process current affairs and generate MCQs
        
        Args:
            title: Article title
            body: Article content (or URL if skip_scraping=True)
            source_url: Optional source URL for fetching source-specific prompts
            skip_scraping: If True, body contains URL and LLM should fetch it
        
        Returns:
            Generated MCQs data
        """
        mode_label = "[SKIP-MODE]" if skip_scraping else "[STANDARD]"
        print(f"  {mode_label} [PROCESSOR] process_mcq_content() - Starting MCQ generation")
        try:
            prompt = self.generate_mcq_prompt(title, body, source_url, skip_scraping=skip_scraping)
            print(f"    [SENDING] Sending to LLM...")
            response = self.llm.generate_json(prompt)
            print(f"    [SUCCESS] LLM response received")
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
    
    def save_mcq_to_database(self, mcq_data: Dict[str, Any], content_type: str = 'currentaffairs_mcq', source_url: str = None) -> List[Dict]:
        """
        Save generated MCQs to database
        
        Args:
            mcq_data: MCQ data from LLM
            content_type: 'currentaffairs_mcq' or 'currentaffairs_descriptive'
            source_url: URL of the source (to fetch content_date from ContentSource)
        
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
            
            # Get content_date from ContentSource if source_url is provided
            year_now = None
            month = None
            day_value = None
            
            if source_url:
                from genai.models import ContentSource
                try:
                    content_source = ContentSource.objects.filter(url=source_url).first()
                    if content_source and content_source.content_date:
                        print(f"      📅 Found ContentSource with date: {content_source.content_date}")
                        year_now = str(content_source.content_date.year)
                        # Month names
                        month_names = {
                            1: "January", 2: "February", 3: "March", 4: "April",
                            5: "May", 6: "June", 7: "July", 8: "August",
                            9: "September", 10: "October", 11: "November", 12: "December"
                        }
                        month = month_names.get(content_source.content_date.month, "January")
                        day_value = content_source.content_date.day
                        print(f"      ✓ Extracted - Year: {year_now}, Month: {month}, Day: {day_value}")
                    else:
                        print(f"      ⚠️  No ContentSource found for URL: {source_url}")
                except Exception as e:
                    print(f"      ❌ Error fetching ContentSource: {str(e)}")
            
            questions = mcq_data.get('questions', [])
            print(f"    📥 Saving {len(questions)} questions...")
            
            for idx, question_data in enumerate(questions, 1):
                # Create MCQ object - use correct fields for each model
                if content_type == 'currentaffairs_mcq':
                    # Map correct answer from LLM (A/B/C/D or 1/2/3/4) to database (1/2/3/4)
                    correct_answer = question_data.get('correct_answer', 'A')
                    if isinstance(correct_answer, str):
                        correct_answer = correct_answer.strip().upper()
                        # Convert letter to number
                        if correct_answer in ['A', 'OPTION_1', '1']:
                            ans_value = 1
                        elif correct_answer in ['B', 'OPTION_2', '2']:
                            ans_value = 2
                        elif correct_answer in ['C', 'OPTION_3', '3']:
                            ans_value = 3
                        elif correct_answer in ['D', 'OPTION_4', '4']:
                            ans_value = 4
                        else:
                            ans_value = 1  # Default fallback
                    else:
                        ans_value = int(correct_answer) if correct_answer else 1
                    
                    # Extract explanation from LLM response
                    explanation = question_data.get('explanation', '')
                    if explanation:
                        # Store explanation in extra field
                        explanation_text = f"Explanation:\n{explanation}"
                    else:
                        explanation_text = ''
                    
                    # Also handle option_a/b/c/d from LLM format
                    # Create the date object from extracted year, month, day
                    if year_now and month and day_value:
                        try:
                            # Convert month name to number
                            month_names_rev = {
                                "January": 1, "February": 2, "March": 3, "April": 4,
                                "May": 5, "June": 6, "July": 7, "August": 8,
                                "September": 9, "October": 10, "November": 11, "December": 12
                            }
                            month_num = month_names_rev.get(month, 1)
                            mcq_date = datetime(int(year_now), month_num, day_value).date()
                        except (ValueError, TypeError):
                            mcq_date = date.today()
                    else:
                        mcq_date = date.today()
                    
                    mcq = model.objects.create(
                        question=question_data.get('question', ''),
                        option_1=question_data.get('option_1', question_data.get('option_a', '')),
                        option_2=question_data.get('option_2', question_data.get('option_b', '')),
                        option_3=question_data.get('option_3', question_data.get('option_c', '')),
                        option_4=question_data.get('option_4', question_data.get('option_d', '')),
                        ans=ans_value,
                        year_now=year_now,
                        month=month,
                        day=mcq_date,
                        creation_time=datetime.now().time(),
                        extra=explanation_text
                    )
                    
                    # Apply categories from LLM classification
                    categories = question_data.get('categories', [])
                    print(f"      [{idx}] Categories from LLM: {categories}")
                    
                    # Map category names to model fields
                    category_mapping = {
                        'Science_Techonlogy': 'Science_Techonlogy',
                        'National': 'National',
                        'International': 'International',
                        'Business_Economy_Banking': 'Business_Economy_Banking',
                        'Environment': 'Environment',
                        'Defence': 'Defence',
                        'Sports': 'Sports',
                        'Art_Culture': 'Art_Culture',
                        'Awards_Honours': 'Awards_Honours',
                        'Persons_in_News': 'Persons_in_News',
                        'Government_Schemes': 'Government_Schemes',
                        'State': 'State',
                        'appointment': 'appointment',
                        'obituary': 'obituary',
                        'important_day': 'important_day',
                        'rank': 'rank',
                        'mythology': 'mythology',
                        'agreement': 'agreement',
                        'medical': 'medical',
                        'static_gk': 'static_gk'
                    }
                    
                    # Set category fields to True if they appear in LLM's categories list
                    for category in categories:
                        if isinstance(category, str):
                            category = category.strip()
                            if category in category_mapping:
                                field_name = category_mapping[category]
                                setattr(mcq, field_name, True)
                                print(f"        ✓ Set {field_name} = True")
                    
                    # Save MCQ with updated category fields
                    mcq.save()
                    
                    saved_mcqs.append({'id': mcq.id, 'question': mcq.question})
                else:
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
    
    def save_descriptive_to_database(self, desc_data: Dict[str, Any], source_url: str = None) -> List[Dict]:
        """
        Save generated descriptive content to database
        
        Args:
            desc_data: Descriptive data from LLM (upper_heading, yellow_heading, key_1-4, all_key_points, categories)
            source_url: URL of the source (to fetch content_date from ContentSource)
        
        Returns:
            List of saved descriptive instances
        """
        from bank.models import currentaffairs_descriptive
        
        print(f"  📋 [SAVER] save_descriptive_to_database()")
        saved_items = []
        
        try:
            # Get content_date from ContentSource if source_url is provided
            year_now = None
            month = None
            day_value = None
            
            if source_url:
                from genai.models import ContentSource
                try:
                    content_source = ContentSource.objects.filter(url=source_url).first()
                    if content_source and content_source.content_date:
                        print(f"      📅 Found ContentSource with date: {content_source.content_date}")
                        year_now = str(content_source.content_date.year)
                        # Month names
                        month_names = {
                            1: "January", 2: "February", 3: "March", 4: "April",
                            5: "May", 6: "June", 7: "July", 8: "August",
                            9: "September", 10: "October", 11: "November", 12: "December"
                        }
                        month = month_names.get(content_source.content_date.month, "January")
                        day_value = content_source.content_date.day
                        print(f"      ✓ Extracted - Year: {year_now}, Month: {month}, Day: {day_value}")
                    else:
                        print(f"      ⚠️  No ContentSource found for URL: {source_url}")
                except Exception as e:
                    print(f"      ❌ Error fetching ContentSource: {str(e)}")
            
            # Create date object
            if year_now and month and day_value:
                try:
                    month_names_rev = {
                        "January": 1, "February": 2, "March": 3, "April": 4,
                        "May": 5, "June": 6, "July": 7, "August": 8,
                        "September": 9, "October": 10, "November": 11, "December": 12
                    }
                    month_num = month_names_rev.get(month, 1)
                    desc_date = datetime(int(year_now), month_num, day_value).date()
                except (ValueError, TypeError):
                    desc_date = date.today()
            else:
                desc_date = date.today()
            
            # Extract fields from LLM response
            upper_heading = desc_data.get('upper_heading', '')
            yellow_heading = desc_data.get('yellow_heading', '')
            key_1 = desc_data.get('key_1', '')
            key_2 = desc_data.get('key_2', '')
            key_3 = desc_data.get('key_3', '')
            key_4 = desc_data.get('key_4', '')
            all_key_points = desc_data.get('all_key_points', '')
            
            print(f"    ✓ Creating descriptive entry: {upper_heading[:50]}...")
            
            # Create descriptive object
            descriptive = currentaffairs_descriptive.objects.create(
                upper_heading=upper_heading,
                yellow_heading=yellow_heading,
                key_1=key_1,
                key_2=key_2,
                key_3=key_3,
                key_4=key_4,
                all_key_points=all_key_points,
                day=desc_date,
                year_now=year_now,
            )
            
            # Apply categories from LLM classification
            categories = desc_data.get('categories', [])
            print(f"      Categories from LLM: {categories}")
            
            # Map category names to model fields
            category_mapping = {
                'Science_Techonlogy': 'Science_Techonlogy',
                'Science_Technology': 'Science_Techonlogy',  # Handle spelling variant
                'National': 'National',
                'International': 'International',
                'Business_Economy_Banking': 'Business_Economy_Banking',
                'Environment': 'Environment',
                'Defence': 'Defence',
                'Sports': 'Sports',
                'Art_Culture': 'Art_Culture',
                'Awards_Honours': 'Awards_Honours',
                'Persons_in_News': 'Persons_in_News',
                'Government_Schemes': 'Government_Schemes',
                'State': 'State',
                'appointment': 'appointment',
                'obituary': 'obituary',
                'important_day': 'important_day',
                'rank': 'rank',
                'mythology': 'mythology',
                'agreement': 'agreement',
                'medical': 'medical',
                'static_gk': 'static_gk'
            }
            
            # Set category fields to True if they appear in LLM's categories list
            for category in categories:
                if isinstance(category, str):
                    category = category.strip()
                    if category in category_mapping:
                        field_name = category_mapping[category]
                        setattr(descriptive, field_name, True)
                        print(f"        ✓ Set {field_name} = True")
            
            # Save descriptive with updated category fields
            descriptive.save()
            saved_items.append(descriptive)
            
            print(f"    ✅ Saved descriptive entry (ID: {descriptive.id})")
            
        except Exception as e:
            print(f"    [ERROR] ERROR saving descriptive: {str(e)}")
            import traceback
            traceback.print_exc()
            logger.error(f"Error saving descriptive content: {str(e)}")
        
        return saved_items
    
    def run_complete_pipeline(self, content_type: str = 'mcq', skip_scraping: bool = False) -> Dict[str, Any]:
        """
        Run the complete pipeline: scrape -> process -> save
        Or skip scraping and send URLs directly to LLM
        
        Args:
            content_type: 'mcq' or 'descriptive'
            skip_scraping: If True, skip web scraping and send URLs directly to LLM
        
        Returns:
            Results dictionary
        """
        print(f"\n{'='*70}")
        print(f"🚀 PIPELINE START - Content Type: {content_type}")
        if skip_scraping:
            print(f"⚡ MODE: Direct-to-LLM (Scraping Skipped)")
        print(f"{'='*70}")
        logger.info(f"Starting Current Affairs pipeline for {content_type} (skip_scraping={skip_scraping})")
        
        # Step 1: Get Content (either scrape or get URLs for direct LLM)
        if skip_scraping:
            # Skip scraping - get URLs directly from ContentSource and send to LLM as-is
            print(f"\n[STEP 1] GETTING URLS FOR DIRECT LLM PROCESSING (No Scraping)...")
            from genai.models import ContentSource
            
            type_mapping = {
                'currentaffairs_mcq': 'currentaffairs_mcq',
                'currentaffairs_descriptive': 'currentaffairs_descriptive'
            }
            source_type = type_mapping.get(content_type, content_type)
            
            sources = ContentSource.objects.filter(
                is_active=True,
                source_type=source_type
            )
            
            if sources.exists():
                # Create content items with URL only (no fetching, no scraping)
                content_list = [
                    {
                        'source_url': str(src.url),
                        'title': f'Direct-to-LLM: {src.url}',
                        'body': f'URL: {src.url}',  # Body contains only the URL
                        'is_url_only': True  # Flag indicating this is URL-only mode
                    }
                    for src in sources
                ]
                print(f"\n✅ [STEP 1] Found {len(content_list)} URLs for direct LLM processing")
                print(f"   Note: URLs will be sent directly to LLM WITHOUT fetching or scraping")
            else:
                print(f"\n⚠ [STEP 1] No content sources found")
                content_list = []
        else:
            # Standard scraping mode
            print(f"\n[STEP 1] SCRAPING...")
            content_list = self.scraper.scrape_from_sources(content_type)
            print(f"\n✅ [STEP 1] Scraped {len(content_list)} articles")
        
        logger.info(f"Retrieved {len(content_list)} content items (skip_scraping={skip_scraping})")
        
        results = {
            'content_type': content_type,
            'articles_scraped': len(content_list),
            'processed_items': [],
            'errors': [],
            'mode': 'direct-to-llm' if skip_scraping else 'standard'
        }
        
        # Step 2: Process and Save
        print(f"\n[STEP 2] PROCESSING & SAVING...")
        for idx, content in enumerate(content_list, 1):
            display_title = content.get('title', 'Unknown')[:50]
            if skip_scraping:
                display_title = content.get('source_url', 'Unknown')[:60]
            
            print(f"\n  [{idx}/{len(content_list)}] Processing: {display_title}...")
            try:
                source_url = content.get('source_url')
                print(f"    Source URL: {source_url}")
                
                if skip_scraping:
                    # In skip-scraping mode, fetch the page content and send to LLM
                    # This way LLM gets actual content without needing online access
                    print(f"    📥 SKIP-MODE: Downloading page content...")
                    try:
                        # Fetch page using Selenium (same scraper instance)
                        print(f"      [FETCH] Attempting Selenium...")
                        html_content = self.scraper.fetch_page_selenium(source_url)
                        
                        if html_content:
                            print(f"      ✅ Successfully fetched {len(html_content)} bytes")
                            # Extract text from HTML
                            soup = BeautifulSoup(html_content, 'html.parser')
                            # Remove script and style elements
                            for script in soup(["script", "style"]):
                                script.decompose()
                            # Get text
                            text = soup.get_text(separator=' ', strip=True)
                            # Clean up whitespace
                            text = ' '.join(text.split())
                            content['body'] = text[:5000]  # Limit to 5000 chars
                            print(f"      ✅ Extracted {len(content['body'])} chars of content")
                        else:
                            print(f"      ❌ Failed to fetch content, falling back to URL")
                            content['body'] = source_url
                    except Exception as e:
                        print(f"      ⚠️  Fetch error: {str(e)}, using URL as fallback")
                        content['body'] = source_url
                
                if content_type == 'currentaffairs_mcq':
                    processed = self.process_mcq_content(content['title'], content['body'], source_url, skip_scraping=skip_scraping)
                    if 'questions' in processed:
                        saved = self.save_mcq_to_database(processed, content_type, source_url)
                        results['processed_items'].extend(saved)
                    else:
                        print(f"    ⚠ No 'questions' key in response")
                else:
                    processed = self.process_descriptive_content(content['title'], content['body'], source_url)
                    # Save descriptive content to database
                    if processed and not processed.get('error'):
                        saved = self.save_descriptive_to_database(processed, source_url)
                        if saved:
                            results['processed_items'].extend(saved)
                            print(f"    ✓ Saved {len(saved)} descriptive item(s) to database")
                    else:
                        print(f"    ⚠ No valid response to save")
            
            except Exception as e:
                print(f"    ❌ ERROR: {str(e)}")
                logger.error(f"Error processing content: {str(e)}")
                results['errors'].append(str(e))
        
        print(f"\n{'='*70}")
        print(f"✅ PIPELINE COMPLETE")
        print(f"  Mode: {'Direct-to-LLM' if skip_scraping else 'Standard Scraping'}")
        print(f"  Total Processed: {len(results['processed_items'])}")
        print(f"  Errors: {len(results['errors'])}")
        print(f"{'='*70}\n")
        logger.info(f"Pipeline completed. Processed {len(results['processed_items'])} items (mode={'direct-to-llm' if skip_scraping else 'standard'})")
        return results


# Utility functions
def fetch_and_process_current_affairs(content_type: str = 'currentaffairs_mcq', skip_scraping: bool = False) -> Dict[str, Any]:
    """
    Main function to fetch and process current affairs content
    
    Args:
        content_type: 'currentaffairs_mcq' or 'current_affairs_descriptive'
        skip_scraping: If True, skip web scraping and send URLs directly to LLM
    
    Returns:
        Processing results
    """
    print("\n" + "="*70)
    print(f"🎯 fetch_and_process_current_affairs() CALLED")
    print(f"   Content Type: {content_type}")
    print(f"   Skip Scraping: {skip_scraping}")
    print("="*70)
    
    try:
        print(f"  📍 Initializing CurrentAffairsProcessor...")
        processor = CurrentAffairsProcessor()
        print(f"  ✓ Processor initialized successfully")
        
        print(f"  📞 Calling processor.run_complete_pipeline('{content_type}', skip_scraping={skip_scraping})...")
        result = processor.run_complete_pipeline(content_type, skip_scraping=skip_scraping)
        print(f"  ✅ Pipeline completed, returning result")
        return result
    except Exception as e:
        print(f"  ❌ ERROR in fetch_and_process_current_affairs: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e), 'processed_count': 0}
