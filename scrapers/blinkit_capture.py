import os
import json
from datetime import datetime

import pandas as pd
from playwright.sync_api import sync_playwright



SEARCH_TERM = input(
    "Enter product to search: "
).strip().lower()

LATITUDE = 12.969426
LONGITUDE = 77.7398991

INITIAL_WAIT = 5000
SCROLL_WAIT = 2500
SCROLL_DISTANCE = 6000



all_products = []
seen_ids = set()


def launch_browser():

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={
            "latitude": LATITUDE,
            "longitude": LONGITUDE
        },
        locale="en-IN",
        timezone_id="Asia/Kolkata"
    )

    page = context.new_page()

    return browser, page


def search_product(page):

    print(f"\nSearching for '{SEARCH_TERM}'...\n")

    page.goto("https://blinkit.com")

    page.wait_for_timeout(INITIAL_WAIT)

    page.locator("input").first.fill(
        SEARCH_TERM
    )

    page.keyboard.press("Enter")

    page.wait_for_timeout(INITIAL_WAIT)


def scroll_to_bottom(page):

    while True:

        previous = page.evaluate(
            "document.body.scrollHeight"
        )

        page.mouse.wheel(
            0,
            SCROLL_DISTANCE
        )

        page.wait_for_timeout(
            SCROLL_WAIT
        )

        current = page.evaluate(
            "document.body.scrollHeight"
        )

        if previous == current:
            break

    print("\nFinished scrolling.\n")


def save_json(filename):

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    path = os.path.join(
        "data/raw",
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_products,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"JSON saved -> {path}")


def save_csv(filename):

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    path = os.path.join(
        "data/processed",
        filename
    )

    df = pd.DataFrame(
        all_products
    )

    df.to_csv(
        path,
        index=False
    )

    print(f"CSV saved -> {path}")


def handle_response(response):

    try:

        if "layout/search" not in response.url:
            return

        data = response.json()

        snippets = data["response"]["snippets"]

        for item in snippets:

            try:

                if "atc_action" not in item["data"]:
                    continue

                product = (
                    item["data"]
                    ["atc_action"]
                    ["add_to_cart"]
                    ["cart_item"]
                )

                pid = product.get(
                    "product_id"
                )

                if not pid:
                    continue

                if pid in seen_ids:
                    continue

                seen_ids.add(pid)

                record = {

                    "platform": "Blinkit",

                    "search_keyword": SEARCH_TERM,

                    "rank": len(all_products) + 1,

                    "scraped_at": datetime.now().isoformat(),

                    "product_id": pid,

                    "product_name": product.get(
                        "product_name"
                    ),

                    "brand": product.get(
                        "brand"
                    ),

                    "price": product.get(
                        "price"
                    ),

                    "mrp": product.get(
                        "mrp"
                    ),

                    "unit": product.get(
                        "unit"
                    ),

                    "inventory": product.get(
                        "inventory"
                    ),

                    "merchant_id": product.get(
                        "merchant_id"
                    ),

                    "rating": item["data"].get(
                        "rating"
                    )

                }

                all_products.append(
                    record
                )

                print(
                    f"[{record['rank']}] {record['product_name']}"
                )

            except Exception as e:

                print(
                    f"Product Parsing Error: {e}"
                )

    except Exception as e:

        print(
            f"Response Processing Error: {e}"
        )


with sync_playwright() as p:

    browser, page = launch_browser()

    page.on(
        "response",
        handle_response
    )

    search_product(page)

    scroll_to_bottom(page)

    print(
        f"\nCollected {len(all_products)} unique products\n"
    )

    filename = SEARCH_TERM.replace(
        " ",
        "_"
    )

    save_json(
        f"{filename}_products.json"
    )

    save_csv(
        f"{filename}_products.csv"
    )

    browser.close()

    print("\nScraping Completed Successfully.")