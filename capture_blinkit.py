from playwright.sync_api import sync_playwright
import json

captured = []

def capture_response(response):
    try:
        if "layout/search" in response.url:
            print("\nFOUND API:")
            print(response.url)

            data = response.json()
            captured.append(data)

            with open("blinkit_response.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            print("\nData saved successfully!")

    except Exception as e:
        print(e)


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.on("response", capture_response)

    page.goto("https://blinkit.com")

    input("""
After Blinkit loads:
1. Search for MILK manually
2. Wait 5 seconds
3. Come back here and press ENTER
""")

    browser.close()