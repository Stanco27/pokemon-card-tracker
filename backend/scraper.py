import requests

def get_universal_stock(tcin, store_id="3991"):
    base_url = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
    
    params = {
        "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
        "tcin": tcin,
        "store_id": store_id,
        "pricing_store_id": store_id,
        "is_bot": "false", 
        "channel": "WEB"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
        "Accept": "application/json",
        "Referer": f"https://www.target.com/p/A-{tcin}"
    }

    session = requests.Session()
    response = session.get(base_url, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return {"error": "Request failed"}