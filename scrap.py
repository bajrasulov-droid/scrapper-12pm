import requests
from bs4 import BeautifulSoup
import json
import csv
import sqlite3

url = "http://books.toscrape.com/"


# ---------------------------
# SCRAPE FUNCTION
# ---------------------------
def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch page")
        return []
    
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    data = []

    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])

        data.append({
            "title": title,
            "currency": currency,
            "price": price
        })

    return data


# ---------------------------
# SAVE TO JSON
# ---------------------------
def save_json(data):
    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print("✓ Saved to books.json")


# ---------------------------
# SAVE TO CSV
# ---------------------------
def save_csv(data):
    with open("books.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "currency", "price"])
        writer.writeheader()
        writer.writerows(data)
    print("✓ Saved to books.csv")


# ---------------------------
# SAVE TO SQLITE DATABASE
# ---------------------------
def save_sqlite(data):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            currency TEXT,
            price REAL
        )
    """)

    cursor.execute("DELETE FROM books")  # optional clean

    for item in data:
        cursor.execute("""
            INSERT INTO books (title, currency, price)
            VALUES (?, ?, ?)
        """, (item["title"], item["currency"], item["price"]))

    conn.commit()
    conn.close()
    print("✓ Saved to books.db (SQLite)")


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def main():
    print("📚 Scraping books...")
    books = scrape_books(url)

    if not books:
        print("No data scraped. Exiting...")
        return

    save_json(books)
    save_csv(books)
    save_sqlite(books)

    print("\n All tasks completed successfully!")


# ---------------------------
# RUN MAIN
# ---------------------------
if __name__ == "__main__":
    main()



#git config --global user.name "Sulov Bajracharya"
#git config --global user.email "bajrasulov@gmail.com"
#git init 
#git stauts => if you want to check what are the status of files
#git add.
#git commit -m "Your message "
# create repository in git hub
# copy paste git code from github
