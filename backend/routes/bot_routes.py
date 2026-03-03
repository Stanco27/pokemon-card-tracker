from flask import Blueprint, request, jsonify
from backend.discord import send_pokemon_alert
from backend.services.bot import target_bot
from backend.scraper import extract_pdp_data, get_pokemon_stock_live, discover_pokemon_tcins
from playwright.sync_api import sync_playwright

bot_bp = Blueprint('bot', __name__)

@bot_bp.route('/start', methods=['POST'])
def start_bot():
    """Starts the background monitoring loop."""
    config = request.json or {}
    result = target_bot.start(config)
    return jsonify(result), 200

@bot_bp.route('/stop', methods=['POST'])
def stop_bot():
    """Stops the background monitoring loop."""
    result = target_bot.stop()
    return jsonify(result), 200

@bot_bp.route('/add', methods=['POST'])
def add_item():
    """Manually add a single TCIN to the running bot."""
    tcin = request.json.get('tcin')
    if not tcin:
        return jsonify({"error": "Missing TCIN"}), 400
        
    result = target_bot.add_item(tcin)
    return jsonify(result), 200


    
@bot_bp.route('/notify', methods=['POST'])
def notify_discord():
    """Endpoint for sending a dynamic Discord alert with live imagery."""
    
    data = request.get_json(silent=True) or {}
    tcin = data.get('tcin')
    title = data.get('title', 'Unknown Product')
    image_url = data.get('image_url')
    
    if not tcin:
        return jsonify({
            "status": "error",
            "message": "Missing TCIN."
        }), 400
    
    try:
        send_pokemon_alert(tcin, title, image_url)
        print(f"🚀 Alert dispatched for {title} (TCIN: {tcin})")
        
        return jsonify({
            "status": "success",
            "data": {"tcin": tcin, "title": title, "has_image": bool(image_url)}
        }), 200
        
    except Exception as e:
        print(f"🔥 Notify Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@bot_bp.route('/test-discord', methods=['POST'])
def test_discord():

    test_tcin = "94681790"
    test_title = "Pokémon TCG: Charizard ex Ultra-Premium Collection"

    test_image_url = "https://assets.pokemon.com/assets/cms2/img/cards/web/SWSH4/SWSH4_EN_20.png"

    print(f"🧪 Triggering test notification for TCIN: {test_tcin}")

    send_pokemon_alert(test_tcin, test_title, test_image_url)

    return {
        "status": "success",
        "mode": "test",
        "item_sent": test_title
    }, 200

@bot_bp.route('/test', methods=['POST'])
def test_single_item():
    """Tests the stock status of a single item (Good for debugging)."""
    config_data = request.json or {}
    tcin = config_data.get('tcin', '95082138') 
    
    try:
        raw_data = get_pokemon_stock_live(tcin)
        item_data = raw_data.get('data', {}).get('product', {}).get('item', {})
        
        title = item_data.get('product_description', {}).get('title', 'Unknown Title')
        eligibility = item_data.get('eligibility_rules', {})
        ship_to_guest = eligibility.get('ship_to_guest', {}).get('is_active', False)

        return jsonify({
            "tcin": tcin,
            "name": title,
            "can_be_shipped": True if ship_to_guest else False
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

@bot_bp.route('/discover', methods=['GET'])
def test_discovery():
    """
    Manually triggers the Auto-Discovery function.
    Returns a JSON list of all found Pokemon TCINs.
    """
    try:
        print("[*] Manual discovery route triggered...")
        
        found_tcins = discover_pokemon_tcins()
        
        return jsonify({
            "message": "Discovery successful",
            "total_found": len(found_tcins),
            "tcins": found_tcins
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Discovery failed", "details": str(e)}), 500
    
@bot_bp.route('/full-test', methods=['POST'])
def run_full_test():
    """Calls the scraper, extracts the data, and triggers the alert."""
    
    data = request.get_json(silent=True) or {}
    tcin = data.get('tcin')
    
    if not tcin:
        return jsonify({"status": "error", "message": "Missing 'tcin' in JSON body"}), 400

    print(f"🚀 Starting Full Pipeline Test for TCIN: {tcin}")
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            page.goto(f"https://www.target.com/p/A-{tcin}", timeout=60000)
            
            print("🔍 Extracting live data...")
            product_data = extract_pdp_data(page)
            
            title = page.locator('[data-test="product-title"]').inner_text()

            print("📨 Sending alert with live data...")
            send_pokemon_alert(
                tcin=tcin,
                title=title,
                image_url=product_data['image_url'],
                price=product_data['price'],
                limit=product_data['limit'],
                is_preorder=product_data['is_preorder']
            )
            
            browser.close()
            
        return jsonify({"status": "success", "message": f"Alert sent for {title}"}), 200

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500