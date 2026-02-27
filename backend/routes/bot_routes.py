from flask import Blueprint, request, jsonify
from backend.scraper import get_universal_stock
from backend.test_api import run_snipe_logic
from backend.services.bot import target_bot, test_bot

bot_bp = Blueprint('bot', __name__)

@bot_bp.route('/start', methods=['POST'])
def start_bot():
    config = request.json
    target_bot.start(config)
    return jsonify({"status": "Bot initialized"}), 200

@bot_bp.route('/stop', methods=['POST'])
def stop_bot():
    target_bot.stop()
    return jsonify({"status": "Bot stopped"}), 200

@bot_bp.route('/test', methods=['POST'])
def test():
    config_data = request.json
    
    if not config_data:
        return jsonify({"error": "No data"}), 400
    
    response = get_universal_stock(config_data.get("tcin"))

    # if "Available" in response:
    #     run_snipe_logic(config_data)
    # else:
    #     return jsonify({"status": "Item not available", "details": response}), 200
    
    return response, 200