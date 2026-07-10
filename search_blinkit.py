from playwright.sync_api import sync_playwright
import json

def handle_response(response):
    try:
        if "search" in response.url:
            print("\nFOUND SEARCH API:")
            print(response.url)

            try:
                data = response.json()

                with open(
                    "blinkit_search.json",
                    "w",
                    encoding="utf-8"
                ) as f:
                    json.dump(data, f, indent=4)

                print("Saved successfully!")

            except:
                pass

    except:
        pass


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.on("response", handle_response)

    page.goto("https://blinkit.com")

    page.wait_for_timeout(5000)

    # Search box
    page.locator("input").first.fill("milk")

    page.keyboard.press("Enter")

    page.wait_for_timeout(10000)

    browser.close()