from flask import Flask, render_template, request, jsonify
import json
import time

app = Flask(__name__)


# Load or create the data file to track boosts
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'coins': 0, 'boosts': [], 'daily_boost_count': 0, 'last_boost_time': 0}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


# Route for the main page
@app.route('/')
def main():
    return render_template('main.html')

# Route for the boost page
@app.route('/boost')
def boost():
    return render_template('boost.html')

@app.route('/buy-boost', methods=['POST'])
def buy_boost():
    data = request.get_json()
    boost_multiplier = data.get('multiplier')

    user_data = load_data()
    current_time = time.time()
    
    # Enforce daily limit (3 boosts max)
    if user_data['daily_boost_count'] >= 3:
        return jsonify({'success': False, 'message': 'Daily boost limit reached'}), 403

    # Enforce 3-hour cooldown
    if current_time - user_data['last_boost_time'] < 3 * 60 * 60:
        remaining_time = int(3 * 60 * 60 - (current_time - user_data['last_boost_time']))
        return jsonify({'success': False, 'message': f'You can buy another boost in {remaining_time // 3600}h {remaining_time % 3600 // 60}m'}), 403

    # Boost is valid, apply it
    user_data['boosts'].append({'multiplier': boost_multiplier, 'start_time': current_time, 'end_time': current_time + 3 * 60 * 60})
    user_data['daily_boost_count'] += 1
    user_data['last_boost_time'] = current_time

    # Save data
    save_data(user_data)

    return jsonify({'success': True, 'message': 'Boost purchased successfully!'})


# Route for the airdrop page
@app.route('/airdrop')
def airdrop():
    return render_template('airdrop.html')

# Route to handle the earning of coins and saving to JSON
@app.route('/earn', methods=['POST'])
def earn_coins():
    data = request.get_json()
    coins = data.get('coins', 0)

    # Load the current data from the JSON file
    try:
        with open('data.json', 'r') as file:
            current_data = json.load(file)
    except FileNotFoundError:
        current_data = {'coins': 0}

    # Update the coin count
    current_data['coins'] = coins

    # Save the updated data back to the JSON file
    with open('data.json', 'w') as file:
        json.dump(current_data, file)

    return jsonify(current_data), 200

@app.after_request
def add_header(response):
    # Cache static files for 1 day
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response



if __name__ == '__main__':
    app.run(debug=True)
