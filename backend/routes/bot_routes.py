from flask import Blueprint, request, jsonify
from backend.services.bot import target_bot
from backend.scraper import get_pokemon_stock_live, discover_pokemon_tcins

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