import requests
from bs4 import BeautifulSoup
import csv
import os
import logging
from database import save_to_db, init_db

logging.basicConfig(filename="scraper.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
}

def fetch_hackernews_articles(pages=1):
    """
    Fetch Hacker News articles.
    :param pages: Number of pages to scrap (each page contains ~30 articles).
    :return: List of dictionnaries caontaining the articles informations.
    """
    articles_list = []

    base_url = "https://news.ycombinator.com/news?p="

    for page in range(1, pages + 1):
        # 1. Download the page
        url = base_url + str(page)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de requête: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        article_rows = soup.find_all("tr", class_="athing submission")

        for row in article_rows:
            # Fetch the article ID
            article_id = row.get('id')

            # 3. Extract the title and URL
            title_tag = row.find("span", class_="titleline").find("a")
            if not title_tag:
                # In case the structure changes
                continue
            
            title = title_tag.text
            link = title_tag.get("href")

            # 4. Fetch the next row
            subtext_row = row.find_next_sibling("tr")
            subtext = subtext_row.find("td", class_="subtext") if subtext_row else None

            if subtext:
                # Find the points
                points_tag = subtext.find("span", class_="score")
                points = int(points_tag.text.split()[0]) if points_tag else 0

                # Find the number of comments
                comments_tag = subtext.find_all("a")[-1]
                comments_text = comments_tag.text
                comments = int(comments_text.split()[0]) if "comment" in comments_text else 0
            else:
                points = 0
                comments = 0

            # Constrct the article object
            article_data = {
                "id": article_id,
                "title": title,
                "link": link,
                "points": points,
                "comments": comments
            }
            articles_list.append(article_data)

    return articles_list

def save_to_csv(articles, filename="data/hackernews_articles.csv"):
    """
    Save the articles lit in a CSV file
    :param articles: list of dictionnaries
    :param filename: CSV file path
    """

    # Verify that the data/ folder exists, otherwise create it
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Determins the columns names (disctionnary keys)
    if articles:
        fieldnames = list(articles[0].keys())
    else:
        return
    
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for art in articles:
            writer.writerow(art)

def main():
    # Example : Scrape the two first pages (~60 articles)
    init_db()
    articles = fetch_hackernews_articles(pages=2)
    logging.info(f"Number of fetched articles : {len(articles)}")

    save_to_csv(articles)
    save_to_db(articles)
    logging.info("Les articles ont été sauvegardés.")

if __name__=='__main__':
    main()
