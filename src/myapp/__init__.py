import os
import sys
from playwright.sync_api import sync_playwright

# 1. Force Playwright to use the local virtual environment
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"


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
        else:
            print("Status: ❌ Chromium is missing. Triggering local installation...")

    print("---------------------------------\n")


if __name__ == "__main__":
    main()
