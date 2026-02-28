import threading
import time
import re
from curl_cffi import requests
from playwright.sync_api import sync_playwright

def get_pokemon_stock_live(tcin, store_id="2786"):
    url = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
    ACTIVE_KEY = "9f36aeafbe60771e321a7cc95a78140772ab3e96"
    
    params = {
        "key": ACTIVE_KEY,
        "tcin": tcin,
        "is_bot": "false",
        "store_id": store_id,
        "pricing_store_id": store_id,
        "channel": "WEB",
        "has_pricing_store_id": "true",
        "include_obsolete": "true"
    }

    headers = {
        "accept": "application/json",
        "referer": f"https://www.target.com/p/A-{tcin}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers, impersonate="chrome110", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        print(f"Request failed for {tcin}: {e}")
        return {}

def get_pokemon_stock_bulk(tcin_list, store_id="2786"):
    """Fetches stock data for up to 30 TCINs simultaneously."""
    url = "https://redsky.target.com/redsky_aggregations/v1/web/product_summary_with_fulfillment_v1"
    ACTIVE_KEY = "9f36aeafbe60771e321a7cc95a78140772ab3e96"
    
    params = {
        "key": ACTIVE_KEY,
        "tcins": ",".join(tcin_list),
        "store_id": store_id,
        "zip": "98109",
        "state": "WA",
        "required_store_id": store_id,
        "channel": "WEB",
        "page": "/s/pokemon cards"
    }

    headers = {
        "accept": "application/json",
        "referer": "https://www.target.com/s?searchTerm=pokemon+cards",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers, impersonate="chrome110", timeout=15)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        print(f"[!] Bulk Request failed: {e}")
        return {}

def discover_pokemon_tcins(max_pages=10):
    print("🎯 Starting deep scrape of ALL available pages...")
    all_tcins = []
    page_num = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        while True:
            offset = page_num * 24
            url = f"https://www.target.com/c/collectible-trading-cards-hobby-collectibles-toys/-/N-27p31Z569t0Zdq4mnZfwtfr?sortBy=newest&Nao={offset}"
            
            print(f"\n📑 [Page {page_num + 1}] Loading offset Nao={offset}...")
            page.goto(url, timeout=60000)
            
            if f"Nao={offset}" not in page.url:
                print(f"🛑 Redirect detected (Current URL: {page.url}). No more pages left.")
                break

            for _ in range(4):
                page.evaluate("window.scrollBy(0, 800)")
                time.sleep(0.5)

            try:
                page.wait_for_selector('[data-test="@web/site-top-of-funnel/ProductCardWrapper"]', timeout=10000)
            except:
                print("🛑 Product grid not found. Ending scrape.")
                break

            cards = page.query_selector_all('[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')
            
            page_tcins = 0
            for card in cards:
                title_elem = card.query_selector('[data-test="@web/ProductCard/title"]')
                if title_elem:
                    raw_title = (title_elem.get_attribute('aria-label') or "").lower()
                    
                    if bool(re.search(r"pok[eé]mon", raw_title)) and "portfolio" not in raw_title and "battle deck" not in raw_title:
                        focus_id = card.get_attribute("data-focusid")
                        if focus_id:
                            tcin = focus_id.split("_")[0]
                            if tcin not in all_tcins:
                                all_tcins.append(tcin)
                                page_tcins += 1

            print(f"✅ Page {page_num + 1} complete. Found {page_tcins} new TCINs.")
            page_num += 1
            
        browser.close()
        print(f"\n🏆 Total unique TCINs collected: {len(all_tcins)}")
        return all_tcins