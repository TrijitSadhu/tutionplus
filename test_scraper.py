import requests
from bs4 import BeautifulSoup
import sys
sys.path.insert(0, 'C:\\Users\\newwe\\Desktop\\tution\\tutionplus\\django\\django_project')

url = 'https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/'
print(f"Fetching: {url}\n")

resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(resp.text, 'html.parser')

# Find article tag
article = soup.find('article')
if article:
    # Get all text from article
    text = article.get_text(strip=True)
    print('ARTICLE TEXT (first 2000 chars):')
    print(text[:2000])
    print("\n\n" + "="*80 + "\n")
    
    # Try to extract the main content body
    # Look for the actual quiz content
    print("Looking for quiz content patterns...\n")
    
    # Find all text nodes and look for question numbers
    for i, p in enumerate(article.find_all('p')[:5]):
        print(f"Paragraph {i}: {p.get_text(strip=True)[:150]}...")
        print()
else:
    print('No article tag found')
    print("Available tags:", [tag.name for tag in soup.find_all(['article', 'main', 'section'], limit=5)])
