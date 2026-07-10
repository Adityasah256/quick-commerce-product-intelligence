from playwright.sync_api import sync_playwright
import json

captured = False

def handle_response(response):
    global captured

    try:
        if "layout/search" in response.url:

            print("\nFOUND SEARCH API")
            print(response.url)

            data = response.json()

            with open(
                "blinkit_search.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(data, f, indent=4)

            print("\nSaved!")

            captured = True

    except Exception as e:
        print(e)


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={
            "latitude": 12.9694264,
            "longitude": 77.7398991
        }
    )

    page = context.new_page()

    page.on("response", handle_response)

    page.goto("https://blinkit.com")

    print("\nPlease:")
    print("1. Allow location")
    print("2. Search MILK")
    print("3. Wait 10 seconds")

    input("\nPress Enter after searching...")

    browser.close()