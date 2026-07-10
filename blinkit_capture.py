from playwright.sync_api import sync_playwright
import json

SEARCH_TERM = "milk"

all_products = []

seen_ids = set()

printed = False

def handle_response(response):
    try:

        if "layout/search" not in response.url:
            return

        data = response.json()

        snippets = data["response"]["snippets"]

        for item in snippets:
            
            global printed

            if not printed:
                print("=" * 80)
                print(item.keys())
                print(item.get("widget_type"))
                print(item["data"].keys())
                printed = True

            try:

                if not printed:

                    print("=" * 100)

                    print(
                        json.dumps(
                            item["data"],
                            indent=2
                        )
                    )

                    printed = True


                product = item["data"]["atc_action"]["add_to_cart"]["cart_item"]

                pid = product["product_id"]

                if pid in seen_ids:
                    continue

                seen_ids.add(pid)

                all_products.append(product)

                print(
                    f"Collected: {product['product_name']}"
                )

            except:
                pass

    except:
        pass


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={
            "latitude":12.9694264,
            "longitude":77.7398991
        }
    )

    page = context.new_page()

    page.on(
        "response",
        handle_response
    )

    page.goto("https://blinkit.com")

    page.wait_for_timeout(5000)

    page.locator("input").first.fill(
        SEARCH_TERM
    )

    page.keyboard.press("Enter")

    page.wait_for_timeout(4000)

    while True:

        previous = page.evaluate(
            "document.body.scrollHeight"
        )

        page.mouse.wheel(
            0,
            6000
        )

        page.wait_for_timeout(2500)

        current = page.evaluate(
            "document.body.scrollHeight"
        )

        if previous == current:
            break

    print(
        f"\nCollected {len(all_products)} products"
    )

    with open(
        "milk_products.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_products,
            f,
            indent=4
        )

    print("JSON Saved!")

    input()

    browser.close()