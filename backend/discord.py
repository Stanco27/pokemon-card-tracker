import requests
from datetime import datetime, timezone
from curl_cffi import requests as stealth_requests

WEBHOOK_URL = ""


def send_pokemon_alert(tcin, title, image_url, price, limit, is_preorder):
    """The Layout function: Formats the data into the 'Wiglett' style."""
    product_url = f"https://www.target.com/p/A-{tcin}"

    description = (
        f"🚨 **Item Restocked**\n\n"
        f"**[{title}]({product_url})**\n\n"
        f"```\n"
        f"SKU              Price          Limit\n"
        f"{tcin}        {price}         {limit}\n"
        f"```\n"
        f"**Pre-order**\n{is_preorder}\n\n"
        f"**TCIN**\n`{tcin}`\n\n"
        f"🔗 **Link**\n"
        f"[Target Store Page]({product_url})"
    )

    payload = {
        "username": "Target Monitor",
        "embeds": [{
            "description": description,
            "color": 16711680,
            "thumbnail": {"url": image_url},
            "footer": {"text": "Target Newest Arrivals Monitor"},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }]
    }
    
    stealth_requests.post(WEBHOOK_URL, json=payload, timeout=10)

def test_discord_ping():
    """Keep this for your /test-discord Flask route"""
    payload = {
        "username": "Bot Health Check",
        "content": "✅ **Internal Test:** Webhook connection is active."
    }
    requests.post(WEBHOOK_URL, json=payload, timeout=10)
