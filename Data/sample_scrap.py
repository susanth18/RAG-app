import requests
from bs4 import BeautifulSoup
url = "https://edition.cnn.com/2025/01/27/tech/deepseek-stocks-ai-china/index.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1')
    if title:
        title = title.get_text(strip=True)
    else:
        title = "Title not found"
        article_body = soup.find('div', class_='article__content')
    if article_body:
        for element in article_body.find_all(['script', 'style', 'iframe', 'figure', 'aside']):
            element.decompose()
        
        content = article_body.get_text(separator='\n', strip=True)
    else:
        content = "Content not found"
    
    print(f"Title: {title}\n")
    print(f"Content:\n{content}")
    
    with open("cnn_article.txt", "w", encoding="utf-8") as file:
        file.write(f"Title: {title}\n\n")
        file.write(content)
    print("\nContent saved to 'cnn_article.txt'")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")