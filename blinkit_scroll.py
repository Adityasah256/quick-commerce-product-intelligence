from playwright.sync_api import sync_playwright
import time

SEARCH_TERM = "milk"

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

    page.goto("https://blinkit.com")

    print("Waiting for Blinkit to load...")
    page.wait_for_timeout(5000)

    # Search
    search_box = page.locator("input").first
    search_box.fill(SEARCH_TERM)

    page.keyboard.press("Enter")

    print("Searching...")
    page.wait_for_timeout(5000)

    previous_height = 0

    while True:

        current_height = page.evaluate(
            "document.body.scrollHeight"
        )

        page.mouse.wheel(0,5000)

        page.wait_for_timeout(3000)

        new_height = page.evaluate(
            "document.body.scrollHeight"
        )

        print(
            f"Previous: {current_height} | New: {new_height}"
        )

        if current_height == new_height:
            break

    print("Finished scrolling!")

    input("Press Enter to close...")

    browser.close()