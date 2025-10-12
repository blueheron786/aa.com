#!/usr/bin/env python3
"""
find_book_links.py <isbn>
---------------------------------
Given an ISBN, prints search URLs for major book retailers
and metadata from Google Books (if available).
"""

import sys
import requests
import urllib.parse

def google_books_info(isbn: str):
    """Fetch metadata and Google Books link from the public API."""
    api = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        r = requests.get(api, timeout=5)
        r.raise_for_status()
        data = r.json()
        if "items" not in data:
            return None
        info = data["items"][0]["volumeInfo"]
        return {
            "title": info.get("title"),
            "authors": ", ".join(info.get("authors", [])),
            "publisher": info.get("publisher"),
            "publishedDate": info.get("publishedDate"),
            "google_books": info.get("infoLink"),
        }
    except Exception as e:
        return None

def build_links(isbn: str):
    """Return a dict of search URLs for major retailers."""
    q = urllib.parse.quote(isbn)
    return {
        "Amazon": f"https://www.amazon.com/s?k={q}",
        "Barnes & Noble": f"https://www.barnesandnoble.com/s/{q}",
        "Bookshop.org": f"https://bookshop.org/books?keywords={q}",
        "Google Books": f"https://books.google.com/books?vid=ISBN:{q}",
        "Goodreads": f"https://www.goodreads.com/search?q={q}",
        "Indigo (Canada)": f"https://www.indigo.ca/en-ca/search/?q={q}",
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: find_links.py <isbn>")
        sys.exit(1)
    isbn = sys.argv[1].replace("-", "").strip()
    print(f"\n🔍 Searching for ISBN: {isbn}\n")

    # Show Google Books info first
    info = google_books_info(isbn)
    if info:
        print("📘 Google Books Metadata:")
        for k, v in info.items():
            if v:
                print(f"  {k}: {v}")
        print()

    # Build and print retailer links
    links = build_links(isbn)
    print("🛒 Retailer Search Links:")
    for name, url in links.items():
        print(f"  {name}: {url}")

    print("\n✅ Copy and open these links to verify actual product pages.")
    print("   Once verified, store the direct URLs in your site metadata.\n")

if __name__ == "__main__":
    main()
