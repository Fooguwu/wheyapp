#!/usr/bin/env python3
"""Check whether a Shopify product is in stock.

Prints a one-line status. When run inside GitHub Actions it also writes
`available`, `title`, `price` and `url` to $GITHUB_OUTPUT for later steps.

Usage:
    python3 check_stock.py                 # checks the default product
    PRODUCT_URL=https://... python3 check_stock.py
"""
import json
import os
import sys
import time
import urllib.request
from urllib.parse import urlsplit, urlunsplit

DEFAULT_URL = "https://agnroots.com/products/agn-roots-grass-fed-whey-3-lbs"


def clean_url(url):
    """Drop tracking query strings and fragments from a product page URL."""
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path.rstrip("/"), "", ""))


def fetch_product(page_url, attempts=3):
    # Every Shopify product page has a JSON twin at the same path plus ".js".
    req = urllib.request.Request(
        page_url + ".js",
        headers={"User-Agent": "Mozilla/5.0 (personal restock checker)", "Accept": "application/json"},
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.load(resp)
        except Exception as exc:
            if attempt == attempts:
                raise
            print(f"Attempt {attempt} failed ({exc}); retrying...", file=sys.stderr)
            time.sleep(5 * attempt)


def main():
    page_url = clean_url(os.environ.get("PRODUCT_URL") or DEFAULT_URL)
    product = fetch_product(page_url)

    available = any(v.get("available") for v in product["variants"])
    title = product["title"]
    price = f"${product['price'] / 100:.2f}"

    print(f"{title}: {'IN STOCK' if available else 'sold out'} ({price}) - {page_url}")

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a") as fh:
            fh.write(f"available={'true' if available else 'false'}\n")
            fh.write(f"title={title}\n")
            fh.write(f"price={price}\n")
            fh.write(f"url={page_url}\n")


if __name__ == "__main__":
    main()
