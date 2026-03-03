import threading
import time
import re
from curl_cffi import requests
from flask import json
from playwright.sync_api import sync_playwright

from backend.discord import send_pokemon_alert

def get_pokemon_stock_live(tcin, store_id="2786", api_key=""):
    url = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
    
    params = {
        "key": api_key,
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
    
def run_consolidated_monitor(tcin_list, api_key, store_id="2786"):
    """
    Uses the 'pdp_client_v1' endpoint from the debug function 
    to ensure image data is always retrieved.
    """
    for tcin in tcin_list:
        url = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
        
        params = {
            "key": api_key,
            "tcin": tcin,
            "store_id": store_id,
            "pricing_store_id": store_id,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                continue

            data = response.json().get("data", {}).get("product", {})
            item = data.get("item", {})
            
            eligibility = item.get("eligibility_rules", {})
            ship_active = eligibility.get("ship_to_guest", {}).get("is_active", False)
            
            fulfillment = data.get("fulfillment", {})
            is_buyable = fulfillment.get("is_buyable", False)
            
            if not (ship_active or is_buyable):
                print(f"⚪ {tcin} is OOS.")
                continue

            title = item.get("product_description", {}).get("title", "Unknown")
            
            enrichment = item.get("enrichment", {})
            images = enrichment.get("images", {})
            image_url = images.get("primary_image_url")
            
            price_node = data.get("price", {})
            price = f"${price_node.get('current_retail')}" if price_node else "N/A"
            order_limit = fulfillment.get("purchase_limit", "No Limit")
            is_preorder = str(enrichment.get("is_preorder", False))

            print(f"✅ HIT! Alerting for {tcin} with verified image URL.")
            send_pokemon_alert(
                tcin=tcin,
                title=title,
                image_url=image_url,
                price=price,
                limit=order_limit,
                is_preorder=is_preorder
            )

        except Exception as e:
            print(f"🔥 Error on {tcin}: {e}")

def debug_target_raw_data(tcin, api_key):
    """
    Pulls the full, raw JSON for a single TCIN to find the exact image path.
    """
    url = "https://redsky.target.com/redsky_aggregations/v1/web/product_summary_with_fulfillment_v1"
    
    params = {
        "key": api_key,
        "tcins": tcin,
        "store_id": "2786",
        "zip": "98109",
        "channel": "WEB",
        "has_pricing_store_id": "true"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": f"https://www.target.com/p/A-{tcin}"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        if response.status_code == 200:
            raw_json = response.json()
            
            products = raw_json.get("data", {}).get("product_summaries", [])
            
            if products:
                print(f"--- RAW DATA FOR TCIN {tcin} ---")
                print(json.dumps(products[0], indent=4))
                
                item = products[0].get("item", {})
                enrichment = item.get("enrichment", {})
                print("\n--- ENRICHMENT KEYS FOUND ---")
                print(enrichment.keys())
            else:
                print("❌ API returned 200 but 'product_summaries' list is empty.")
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"🔥 Script Error: {e}")

def debug_image_path(tcin, api_key):
    url = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1" # Trying the client-side endpoint
    
    params = {
        "key": api_key,
        "tcin": tcin,
        "store_id": "2786",
        "pricing_store_id": "2786",
        "is_bot": "false"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        item = data.get("data", {}).get("product", {}).get("item", {})
        enrichment = item.get("enrichment", {})
        images = enrichment.get("images", {})
        
        print(f"--- PDP CLIENT IMAGES FOR {tcin} ---")
        if images:
            print(json.dumps(images, indent=4))
        else:
            print("❌ Images still missing. Target is hiding them for this item.")
            
    except Exception as e:
        print(f"🔥 Error: {e}")

def get_pokemon_stock_bulk(tcin_list, store_id="2786", api_key=""):
    """Fetches stock data for up to 30 TCINs simultaneously."""
    url = "https://redsky.target.com/redsky_aggregations/v1/web/product_summary_with_fulfillment_v1"
    
    params = {
        "key": api_key,
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
    
def extract_pdp_data(page):
    """Refined extraction with .first to avoid strict mode violations."""
    
    page.wait_for_selector('h1[data-test="product-title"]', timeout=10000)
    
    title = page.locator('h1[data-test="product-title"]').first.inner_text()
    price = page.locator('[data-test="product-price"]').first.inner_text()

    img_elem = page.locator('div[data-test="carousel"] img').first
    image_url = img_elem.get_attribute('src') if img_elem.count() > 0 else None

    badge = page.locator('[data-test="product-badge"]').first
    badge_text = badge.inner_text().lower() if badge.count() > 0 else ""
    
    is_preorder = "True" if page.locator('button:has-text("Pre-order")').count() > 0 else "False"
    
    limit_match = re.search(r'limit\s+(\d+)', badge_text)
    order_limit = limit_match.group(1) if limit_match else "No Limit"

    return {
        "title": title,
        "price": price,
        "image_url": image_url,
        "limit": order_limit,
        "is_preorder": is_preorder
    }

def test_target_api_with_limit(tcin, api_key):
    url = "https://redsky.target.com/redsky_aggregations/v1/web/product_summary_with_fulfillment_v1"
    
    params = {
        "key": api_key,
        "tcins": tcin,
        "store_id": "2786",
        "zip": "98109",
        "channel": "WEB",
        "required_store_id": "2786",
        "has_pricing_store_id": "true"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": f"https://www.target.com/p/A-{tcin}"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get("data", {}).get("product_summaries", [])
            
            if products:
                p = products[0]
                item = p.get("item", {})
                
                is_preorder = item.get("enrichment", {}).get("is_preorder", False)
                
                limit = p.get("fulfillment", {}).get("purchase_limit", "No Limit")
                
                price = p.get("price", {}).get("current_retail", "N/A")
                title = item.get("product_description", {}).get("title", "Unknown")

                print(f"✅ Data for {tcin}:")
                print(f"Title: {title}")
                print(f"Price: ${price}")
                print(f"Order Limit: {limit}")
                print(f"Is Pre-order: {is_preorder}")
                
                return {
                    "title": title,
                    "price": f"${price}",
                    "limit": limit,
                    "is_preorder": str(is_preorder)
                }
    except Exception as e:
        print(f"🔥 API Error: {e}")
    return None
