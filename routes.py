from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from fire import get_user_data, save_coin_data, update_boost_data
import json
import time

routes = Blueprint('routes', __name__)



@routes.route('/')
def index():
    # Example of fetching user_data from Firebase
    user_data = get_user_data()  # Ensure this function works and returns data
    return render_template('index.html', user_data=user_data)



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



@routes.route('/boost')
def boost_page():
    user_data = get_user_data()  # Fetch user data (replace with Firebase logic)
    return render_template('boost.html', user_data=user_data)

@routes.route('/buy-boost', methods=['POST'])
def buy_boost():
    data = request.get_json()
    boost_type = data.get('boost_type')
    user_data = get_user_data()

    # Define the cost for each boost type
    boost_costs = {
        '2x': 5000,
        '3x': 10000,
        '10x': 100000,
        'full': 150000
    }

    # Validate the selected boost type
    if boost_type not in boost_costs:
        return jsonify({'message': 'Invalid boost type selected.'}), 400

    # Check if the user has enough coins
    cost = boost_costs[boost_type]
    if user_data['coins'] < cost:
        return jsonify({'message': 'Not enough coins!'}), 400

    # Deduct coins and apply boost
    user_data['coins'] -= cost
    if boost_type == 'full':
        user_data['boost_type'] = 'full'
        user_data['boost_multiplier'] = 5  # Maximum boost effect
    else:
        user_data['boost_type'] = boost_type
        user_data['boost_multiplier'] = {'2x': 2, '3x': 3, '10x': 5}[boost_type]

    # Optionally, set a boost expiration (3 hours from now)
    user_data['boost_expires'] = time.time() + 3 * 60 * 60  # 3 hours in seconds

    # Save the updated user data (implement Firebase or database saving logic)
    update_boost_data(user_data)

    return jsonify({
        'message': f'{boost_type.capitalize()} boost purchased!',
        'coins': user_data['coins']
    })

