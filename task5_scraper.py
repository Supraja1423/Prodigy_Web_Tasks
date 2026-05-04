import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_books():
    data = []

    for page in range(1, 4):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed page {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            name = book.h3.a["title"]
            price = book.find("p", class_="price_color").text

            rating_class = book.find("p", class_="star-rating")["class"][1]

            rating_map = {
                "One": 1, "Two": 2, "Three": 3,
                "Four": 4, "Five": 5
            }

            rating = rating_map.get(rating_class, 0)

            data.append({
                "Name": name,
                "Price": price,
                "Rating": rating
            })

    return data


def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("products.csv", index=False)
    print("✅ Saved as products.csv")


if __name__ == "__main__":
    print("🔄 Scraping...")
    data = scrape_books()
    save_to_csv(data)
    print("🎉 Done!")