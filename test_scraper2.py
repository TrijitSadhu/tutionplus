import requests
from bs4 import BeautifulSoup

url = 'https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/'
print(f"Fetching: {url}\n")

resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(resp.text, 'html.parser')

# Find main tag
main = soup.find('main')
if main:
    print("MAIN TAG STRUCTURE:")
    print("="*80)
    
    # Get h1
    h1 = main.find('h1')
    if h1:
        print(f"H1 Title: {h1.get_text(strip=True)}\n")
    
    # Find the actual quiz content - look for numbered questions or strong tags
    print("\nLooking for quiz questions...")
    questions = []
    
    # Method 1: Look for <p> tags with <strong> (numbered questions)
    for p in main.find_all('p'):
        text = p.get_text(strip=True)
        if text and len(text) > 20:  # Skip very short text
            print(f"P tag: {text[:100]}...")
            questions.append(text[:200])
            if len(questions) >= 5:
                break
    
    print(f"\n\nFound {len(questions)} potential question blocks")
    
    # Try finding with different class names
    print("\n\nSearching for divs with specific classes...")
    divs = main.find_all('div', limit=10)
    for i, div in enumerate(divs):
        classes = div.get('class', [])
        text = div.get_text(strip=True)
        if text and len(text) > 30 and len(text) < 500:
            print(f"Div {i}: class={classes}, text={text[:80]}...")
else:
    print('No main tag found')
    
# Also check page title/meta
title = soup.find('title')
if title:
    print(f"\nPage Title: {title.get_text()}")
    
# Check meta description
meta_desc = soup.find('meta', {'name': 'description'})
if meta_desc:
    print(f"Meta Description: {meta_desc.get('content', '')}")
