import os
import sys
from playwright.sync_api import sync_playwright

# 1. Default to package-local browsers, while allowing external override.
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")

GOOGLE_SELECTOR = (
    "body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > "
    "div.A8SBwf > div.FPdoLc.lJ9FBc > center > input.RNmpXc"
)


def main():
    print("\n--- 🔍 Environment Debug Info ---")

    # 2. Print the active Python path
    print(f"Python Executable: {sys.executable}")

    with sync_playwright() as p:
        # 3. Get Playwright's expected Chromium path
        chromium_path = p.chromium.executable_path
        print(f"Chromium Target Path: {chromium_path}")

        # 4. Check if the browser is actually installed there right now
        if os.path.exists(chromium_path):
            print("Status: ✅ Chromium is currently installed locally!")

            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto("https://www.google.com", wait_until="domcontentloaded")
                value = page.locator(GOOGLE_SELECTOR).get_attribute("value")
                print(f"Selector value: {value}")
            finally:
                browser.close()
        else:
            print("Status: ❌ Chromium is missing. Triggering local installation...")

    print("---------------------------------\n")


if __name__ == "__main__":
    main()
