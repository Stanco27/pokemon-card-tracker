from curl_cffi import requests
import json

def get_universal_stock(tcin, store_id="3991"):
    # Current high-stability endpoint
    base_url = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_v3"
    
    # YOUR NEW PINGPROXIES CREDENTIALS
    # Format: username:password@endpoint:port
    # Note: Replace 'residential.pingproxies.com:8000' with the actual 
    # server address provided in your PingProxies dashboard.
    proxy_user = "102567_ZjdwR"
    proxy_pass = "NGn9ez1bVu"
    proxy_host = "residential.pingproxies.com:8000" 
    
    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}"
    proxies = {"http": proxy_url, "https": proxy_url}

    # Use the key you extracted from your browser session
    ACTIVE_KEY = "9f36aeafbe60771e321a7cc95a78140772ab3e96" 

    params = {
        "key": ACTIVE_KEY,
        "tcin": tcin,
        "store_id": store_id,
        "pricing_store_id": store_id,
        "is_bot": "false",
        "channel": "WEB",
        "required_fields": "fulfillment_options,location_and_quantity,pricing"
    }
    
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "referer": f"https://www.target.com/p/A-{tcin}",
        "origin": "https://www.target.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        # Impersonate Chrome to bypass TLS fingerprinting
        response = requests.get(
            base_url, 
            params=params, 
            headers=headers, 
            proxies=proxies,
            impersonate="chrome110", 
            timeout=15
        )
        
        if response.status_code == 200:
            # If this hits, the data will be massive. 
            # This is exactly what we need for the raw dump.
            return response.json()
            
        return {
            "error_code": response.status_code,
            "msg": "Target is still rejecting the request.",
            "raw_body": response.text
        }
    except Exception as e:
        return {"error": f"Proxy connection failed: {str(e)}"}