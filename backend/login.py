import os
from playwright.sync_api import sync_playwright

def ensure_login(session_id):
    user_data_dir = os.path.join(os.getcwd(), f"sessions/{session_id}")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.pages[0]
        page.goto("https://www.target.com", wait_until="domcontentloaded")

        try:
            page.wait_for_selector("text=Hi, ", timeout=5000)
            return True
        except:
            page.wait_for_selector("text=Hi, ", timeout=0)
            return True
        finally:
            context.close()