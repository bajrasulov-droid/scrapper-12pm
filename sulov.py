import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    all_books = []

    for book in books:
        title = book.h3.a['title']
        price_text = book.find("p", class_="price_color").text
        
        currency = price_text[0]      # keeps £
        price = float(price_text[1:])

        all_books.append([title, currency, price])

    return all_books


books = scrape_books(url)

# ✅ Save to CSV
with open("books.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(["Title", "Currency", "Price"])
    
    # Write rows
    writer.writerows(books)
