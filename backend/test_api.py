import os
import time
from playwright.sync_api import sync_playwright

def run_snipe_logic(config_data):
    session_id = config_data.get("session_id")
    tcin = config_data.get("tcin")
    interval = config_data.get("interval")
    user_data_dir = os.path.join(os.getcwd(), f"sessions/{session_id}")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.pages[0]

        while True:
            try:
                page.goto(f"https://www.target.com/p/A-{tcin}", wait_until="domcontentloaded")
                shipping_tile = page.locator('[data-test="fulfillment-cell-shipping"]')
                
                if shipping_tile.is_visible() and "Out of stock" not in shipping_tile.inner_text():
                    shipping_tile.click()
                    
                    js_click = f"""
                    (async () => {{
                        const selector = '#addToCartButtonOrTextIdFor{tcin}';
                        for (let i = 0; i < 30; i++) {{
                            const btn = document.querySelector(selector);
                            if (btn && !btn.disabled) {{
                                btn.click();
                                return "SUCCESS";
                            }}
                            await new Promise(r => setTimeout(r, 200));
                        }}
                        return "TIMEOUT";
                    }})();
                    """
                    if page.evaluate(js_click) == "SUCCESS":
                        page.wait_for_timeout(1500)
                        decline = page.locator('button:has-text("Decline"), button:has-text("No thanks")').first
                        if decline.is_visible():
                            decline.click()
                        
                        if config_data.get("auto_checkout"):
                            page.goto("https://www.target.com/checkout", wait_until="load")
                        break
                
                time.sleep(interval)
            except Exception:
                time.sleep(interval)

        page.wait_for_timeout(60000)
        context.close()