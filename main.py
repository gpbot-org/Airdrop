from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import time
import json
from fire import get_user_data, save_user_data

app = Flask(__name__)
app.secret_key = "gpbot_the_best"  # Ensure you set a secure secret key for session management

@app.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return "User not logged in", 403  # Handle unauthenticated user
    user_data = get_user_data(user_id)  # Fetch user data for the homepage
    return render_template('index.html', user_data=user_data)

@app.route('/boost')
def boost_page():
    user_id = session.get('user_id')
    if not user_id:
        return "User not logged in", 403  # Handle unauthenticated user
    user_data = get_user_data(user_id)
    return render_template('boost.html', user_data=user_data)

@app.route('/buy-boost', methods=['POST'])
def buy_boost():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in!'}), 403

    data = request.get_json()
    boost_type = data.get('boost_type')
    user_data = get_user_data(user_id)

    # Define the cost for each boost type
    boost_costs = {
        '2x': 5000,
        '3x': 10000,
        '10x': 100000,
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
    user_data['boosts'][boost_type]['active'] = True
    user_data['boosts'][boost_type]['expiry'] = time.time() + 3 * 60 * 60  # 3 hours

    save_user_data(user_id, user_data)  # Save the updated user data

    return jsonify({'message': f'{boost_type.capitalize()} boost purchased!', 'coins': user_data['coins']})

@app.route('/airdrop')
def airdrop():
    """Airdrop page showing listings."""
    return render_template('airdrop.html')

@app.route('/login', methods=['GET'])
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
            save_user_data(user_id, {"coins": 0, "boosts": {"2x": {"active": False, "expiry": None},
                                                              "3x": {"active": False, "expiry": None},
                                                              "10x": {"active": False, "expiry": None}}})  # Initialize with 0 coins and boost data
        session['user_id'] = user_id  # Store user_id in session
        return redirect(url_for('index'))
    
    except json.JSONDecodeError:
        return "Error decoding Telegram data", 500

@app.route('/save_coins', methods=['POST'])
def save_coins():
    """Save coin data when user taps or purchases boost."""
    data = request.json
    user_id = data.get('user_id')
    coins = data.get('coins')
    
    if user_id and coins is not None:
        user_data = get_user_data(user_id)
        user_data['coins'] = coins
        save_user_data(user_id, user_data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
