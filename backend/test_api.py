import os
import time
from playwright.sync_api import sync_playwright

def run_snipe_logic(config_data):
    session_id = config_data.get("session_id")
    tcin = config_data.get("tcin")
    qty = config_data.get("quantity", 1)
    interval = float(config_data.get("interval", 0.5)) 
    user_data_dir = os.path.join(os.getcwd(), f"sessions/{session_id}")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.pages[0]
        
        page.goto(f"https://www.target.com/p/A-{tcin}", wait_until="domcontentloaded")

        while True:
            if page.is_closed():
                break

            try:
                page.reload(wait_until="commit")
                
                shipping_tile = page.locator('[data-test="fulfillment-cell-shipping"]')
                
                if shipping_tile.is_visible(timeout=100) and "Out of stock" not in shipping_tile.inner_text():
                    shipping_tile.click(force=True)

                    if qty > 1:
                        try:
                            qty_selector = page.locator('select[data-test="quantity-select"]')
                            if qty_selector.is_visible(timeout=500):
                                qty_selector.select_option(str(qty))
                        except:
                            print(f"Could not set quantity to {qty}, item may be limited.")
                    
                    js_click = f"""
                    (async () => {{
                        const selector = '#addToCartButtonOrTextIdFor{tcin}';
                        for (let i = 0; i < 50; i++) {{
                            const btn = document.querySelector(selector);
                            if (btn && !btn.disabled) {{
                                btn.click();
                                return "SUCCESS";
                            }}
                            await new Promise(r => setTimeout(r, 50));
                        }}
                        return "TIMEOUT";
                    }})();
                    """
                    
                    if page.evaluate(js_click) == "SUCCESS":
                        page.wait_for_timeout(500)
                        
                        if config_data.get("auto_checkout"):
                            page.goto("https://www.target.com/checkout", wait_until="domcontentloaded")
                        break
                
                time.sleep(interval)
                
            except Exception as e:
                if "Target page, context or browser has been closed" in str(e):
                    break
                print(f"Engine Error: {e}")
                time.sleep(interval)

        context.close()