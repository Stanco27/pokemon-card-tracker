from flask import Blueprint, request, jsonify
from services.bot import target_bot

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