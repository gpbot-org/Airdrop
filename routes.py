from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from fire import get_user_data, save_coin_data, update_boost_data
import json


routes = Blueprint('routes', __name__)



@routes.route('/')
def index():
    """Main page where user can tap to earn coins."""
    return render_template('index.html')

@routes.route('/boost')
def boost():
    """Boost page for purchasing coin boosts."""
    return render_template('boost.html')

@routes.route('/airdrop')
def airdrop():
    """Airdrop page showing listings."""
    return render_template('airdrop.html')

@routes.route('/login', methods=['GET'])
def login():
    tg_web_app_data = request.args.get('tgWebAppData', None)
    if not tg_web_app_data or tg_web_app_data == 'null':
        return "Error: Invalid Telegram Data", 404
    
    try:
        tg_data = json.loads(tg_web_app_data)
        user_id = tg_data['user']['id']
        user_name = tg_data['user']['username']
        
        # Fetch or create user in Firebase
        user_data = get_user_data(user_id)
        if not user_data:
            save_coin_data(user_id, {"coins": 0})  # Initialize with 0 coins
        return redirect(url_for('index', user_id=user_id))
    
    except json.JSONDecodeError:
        return "Error decoding Telegram data", 500

@routes.route('/save_coins', methods=['POST'])
def save_coins():
    """Save coin data when user taps or purchases boost."""
    data = request.json
    user_id = data.get('user_id')
    coins = data.get('coins')
    
    if user_id and coins is not None:
        save_coin_data(user_id, coins)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@routes.route('/buy_boost', methods=['POST'])
def buy_boost():
    """Buy boost and update user's coins and boost data."""
    data = request.json
    user_id = data.get('user_id')
    boost_type = data.get('boost_type')
    
    # Assuming you have a boost price list
    boost_prices = {"2x": 5000, "3x": 10000, "10x": 100000}
    
    user_data = get_user_data(user_id)
    current_coins = user_data['coins'] if user_data else 0
    
    if boost_type in boost_prices:
        boost_price = boost_prices[boost_type]
        if current_coins >= boost_price:
            # Deduct the price and update boost info
            new_coin_count = current_coins - boost_price
            save_coin_data(user_id, new_coin_count)
            update_boost_data(user_id, {"boost_type": boost_type, "end_time": "3h from now"})
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Not enough coins"}), 400
    return jsonify({"status": "error"}), 400

