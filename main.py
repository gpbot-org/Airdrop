from flask import Flask, request, jsonify, render_template, session
import time
from fire import get_user_data, save_user_data

app = Flask(__name__)
app.secret_key = "gpbot_the_best"  # Ensure you set a secret key for session management

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
        'full': 150000  # Example full boost cost
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

if __name__ == '__main__':
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

