import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os

# Input and Output Paths
output_dir = r"C:\AI\Python\output_data"  # Directory for saving scraped news data
output_file = os.path.join(output_dir, "ipl_2020_ndtv_news.csv")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# URL to scrape
url = "https://sports.ndtv.com/ipl-2020/news"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"
}

# Step 1: Fetch the page and extract news articles
try:
    print(f"Fetching news from {url}...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Find news articles (adjust class names based on HTML inspection)
    articles = soup.find_all("li", class_="cnt_lst_li")  # Adjust class name if needed

    news_data = []
    for article in articles:
        # Extract title
        title_tag = article.find("a", class_="item-title")
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        # Extract date
        date_tag = article.find("span", class_="lst_publsh-time")
        date_text = date_tag.get_text(strip=True) if date_tag else "No date"
        try:
            date = datetime.strptime(date_text, "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            date = "Unknown"

        # Extract article body (summary)
        body_tag = article.find("div", class_="description")
        body = body_tag.get_text(strip=True) if body_tag else "No body"

        # Filter for IPL 2020-related articles
        if "IPL 2020" in title or "match" in title.lower() or "final" in title.lower():
            news_data.append({
                "title": title,
                "date": date,
                "body": body
            })

    # Save news data to CSV
    if news_data:
        df_news = pd.DataFrame(news_data)
        df_news.to_csv(output_file, index=False)
        print(f"Extracted {len(df_news)} news articles and saved to {output_file}")
        print(df_news.head())
    else:
        print("No relevant IPL 2020 news articles found on the page.")

except requests.RequestException as e:
    print(f"Error fetching {url}: {str(e)}")