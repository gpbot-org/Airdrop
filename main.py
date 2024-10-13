from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import time
import json
from fire import get_user_data, save_user_data
import urllib.parse

app = Flask(__name__)
app.secret_key = "gpbot_the_best"  # Set a secure secret key for session management

@app.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('telegram_login'))  # Redirect to login if not authenticated
    user_data = get_user_data(user_id)
    return render_template('index.html', user_data=user_data)

@app.route('/boost')
def boost_page():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('telegram_login'))  # Redirect to login if not authenticated
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
def telegram_login():
    tg_web_app_data = request.args.get('tgWebAppData', None)
    if tg_web_app_data and tg_web_app_data != 'null':
        tg_web_app_data = urllib.parse.unquote(tg_web_app_data)
        
        try:
            tg_data = json.loads(tg_web_app_data)
            user_id = tg_data['user']['id']
            user_name = tg_data['user'].get('username', 'Unknown')

            session['user_id'] = user_id
            session['user_name'] = user_name
            return redirect(url_for('index'))
        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Error decoding JSON"}), 400
        except KeyError:
            return jsonify({"status": "error", "message": "Missing user information"}), 400
    return jsonify({"status": "error", "message": "Invalid login data"}), 400

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
