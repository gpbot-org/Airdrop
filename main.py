import requests
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import json
import urllib.parse
import time
from fire import get_user_data, save_user_data

app = Flask(__name__)
app.secret_key = "gpbot_the_best"  # Secure your secret key

BOT_TOKEN = "8006330572:AAGqjETC6oqMaJH5MUIJGE_k3EOeHDoxbac"
WEB_APP_URL = "https://airdrop-2v66.onrender.com/login"  # Your web app URL

@app.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return "User not logged in", 403
    user_data = get_user_data(user_id)
    return render_template('index.html', user_data=user_data)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update and 'text' in update['message']:
        chat_id = update['message']['chat']['id']
        text = update['message']['text']

        if text == '/start':
            user_id = update['message']['from']['id']
            user_name = update['message']['from'].get('username', 'Unknown')

            auth_url = f"{WEB_APP_URL}?tgWebAppData={generate_auth_data(user_id, user_name)}"
            send_message(chat_id, f"Welcome {user_name}! Click [here]({auth_url}) to login to the web app.", True)

    return '', 200

def send_message(chat_id, text, disable_web_page_preview=False):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': disable_web_page_preview
    }
    requests.post(url, json=payload)

def generate_auth_data(user_id, user_name):
    data = {
        "user": {
            "id": user_id,
            "username": user_name
        }
    }
    return urllib.parse.quote(json.dumps(data))

@app.route('/login', methods=['GET'])
def telegram_login():
    tg_web_app_data = request.args.get('tgWebAppData', None)
    if not tg_web_app_data or tg_web_app_data == 'null':
        return "Error: Invalid Telegram Data", 404
    
    try:
        tg_web_app_data = urllib.parse.unquote(tg_web_app_data)
        tg_data = json.loads(tg_web_app_data)

        user_id = tg_data['user']['id']
        user_name = tg_data['user'].get('username', 'Unknown')

        user_data = get_user_data(user_id)
        if not user_data:
            user_data = {
                "coins": 0,
                "boosts": {
                    "2x": {"active": False, "expiry": None},
                    "3x": {"active": False, "expiry": None},
                    "10x": {"active": False, "expiry": None}
                }
            }
            save_user_data(user_id, user_data)

        session['user_id'] = user_id
        session['user_name'] = user_name
        return redirect(url_for('index'))

    except json.JSONDecodeError:
        return "Error decoding Telegram data", 500
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/boost')
def boost_page():
    user_id = session.get('user_id')
    if not user_id:
        return "User not logged in", 403
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

    boost_costs = {
        '2x': 5000,
        '3x': 10000,
        '10x': 100000,
    }

    if boost_type not in boost_costs:
        return jsonify({'message': 'Invalid boost type selected.'}), 400

    cost = boost_costs[boost_type]
    if user_data['coins'] < cost:
        return jsonify({'message': 'Not enough coins!'}), 400

    user_data['coins'] -= cost
    user_data['boosts'][boost_type]['active'] = True
    user_data['boosts'][boost_type]['expiry'] = time.time() + 3 * 60 * 60  # 3 hours

    save_user_data(user_id, user_data)

    return jsonify({'message': f'{boost_type.capitalize()} boost purchased!', 'coins': user_data['coins']})

@app.route('/airdrop')
def airdrop():
    return render_template('airdrop.html')

if __name__ == '__main__':
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
