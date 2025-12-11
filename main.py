import cloudscraper
from bs4 import BeautifulSoup

def get_most_popular_news_content():
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

def get_most_popular_news(html_content):
    data = []
    if not html_content:
        return data

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('a', class_=lambda x: x and 'whitespace-normal' in x and 'font-bold' in x)
    description = soup.find_all('p', class_=lambda x: x and 'mt-[0.5rem] hidden overflow-hidden text-xs leading-[1.38rem] md:block' in x)
    provider = soup.find_all('span', attrs={'data-test': 'news-provider-name'}, class_=lambda x: x and 'shrink-0 text-xs leading-4' in x)
    last_update = soup.find_all('time', class_=lambda x: x and 'mx-1 shrink-0 text-xs leading-4' in x)

    for idx, article in enumerate(articles):
        title = article.get_text(strip=True)
        link = article.get('href')

        if link and link.startswith('/'):
            link = f"https://www.investing.com{link}"

        if title and link:
            data.append(
                {
                    "title": title, 
                    "link": link, 
                    "description": description[idx].get_text(strip=True), 
                    "provider": provider[idx].get_text(strip=True),
                    "last_update": last_update[idx].get_text(strip=True),
                }
            )

    return data

if __name__ == "__main__":
    html_content = get_most_popular_news_content()
    data = get_most_popular_news(html_content)
    print(data)
