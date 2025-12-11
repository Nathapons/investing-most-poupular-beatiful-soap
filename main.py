import cloudscraper
from bs4 import BeautifulSoup

def fetch_investing_news():
    url = "https://www.investing.com/news/most-popular-news"
    
    # Create scraper instance
    scraper = cloudscraper.create_scraper() 
    
    try:
        response = scraper.get(url)
        
        if response.status_code == 200:
            print("Success! Downloaded HTML.")
            return response.text
        else:
            print(f"Failed. Status Code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_news(html_content):
    if not html_content:
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find articles based on the identified classes
    # We look for <a> tags that contain 'whitespace-normal' and 'font-bold' in their class attribute
    articles = soup.find_all('a', class_=lambda x: x and 'whitespace-normal' in x and 'font-bold' in x)

    print(f"Found {len(articles)} articles.")

    for article in articles:
        title = article.get_text(strip=True)
        link = article.get('href')
        
        # Handle relative URLs
        if link and link.startswith('/'):
            link = f"https://www.investing.com{link}"
            
        if title and link:
            print(f"Title: {title}")
            print(f"Link: {link}")
            print("-" * 40)

if __name__ == "__main__":
    html_content = fetch_investing_news()
    parse_news(html_content)
