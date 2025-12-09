import requests
from bs4 import BeautifulSoup
import sqlite3
import csv

# -----------------------------
# Step 1: Scrape books
# -----------------------------
url = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    all_books = []

    for book in books:
        title = book.h3.a['title']
        price_text = book.find("p", class_="price_color").text
        
        currency = price_text[0]      # keep £
        price = float(price_text[1:])

        all_books.append((title, currency, price))  # tuple for SQLite

    return all_books

books = scrape_books(url)

# -----------------------------
# Step 2: Save to SQLite
# -----------------------------
conn = sqlite3.connect("books.db")  # creates database file
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    currency TEXT,
    price REAL
)
""")

# Insert books into table
cursor.executemany("INSERT INTO books (title, currency, price) VALUES (?, ?, ?)", books)

conn.commit()

# -----------------------------
# Step 3: Export SQLite to CSV
# -----------------------------
cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()

with open("books_export.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Write header row
    writer.writerow([i[0] for i in cursor.description])
    
    # Write data rows
    writer.writerows(rows)

conn.close()

print("Scraping ✅ | Saved to SQLite ✅ | Exported to CSV ✅")
