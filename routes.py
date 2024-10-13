from flask import Blueprint, render_template, request, redirect, url_for
from fire import get_user, create_user, update_user, save_user_coins
import json

routes = Blueprint('routes', __name__)

@routes.route('/')
def main():
    user_id = request.args.get('user_id')  # Extract user_id from query parameters
    user_data = get_user(user_id)

    if user_data is None:
        # Create new user with initial coins and boosts
        create_user(user_id, {"coins": 0, "boosts": []})
        user_data = get_user(user_id)

    # Increment coins on tap
    if request.method == 'POST':  # Assuming a POST request for tapping
        user_data['coins'] += 1  # Increase coins by 1 for each tap
        save_user_coins(user_id, user_data['coins'])  # Save updated coins to Firebase

    return render_template('main.html', user_data=user_data)


@routes.route('/boost', methods=['GET', 'POST'])
def boost():
    user_id = request.args.get('user_id')
    user_data = get_user(user_id)

    if request.method == 'POST':
        boost_type = request.form['boost_type']
        coins = user_data.get('coins', 0)

        # Logic for buying boosts based on type and new prices
        if boost_type == '2x' and coins >= 5000:
            user_data['coins'] -= 5000
            user_data['boosts'].append({'type': '2x', 'duration': 3})  # Add boost with duration
        elif boost_type == '3x' and coins >= 10000:
            user_data['coins'] -= 10000
            user_data['boosts'].append({'type': '3x', 'duration': 3})
        elif boost_type == '10x' and coins >= 100000:
            user_data['coins'] -= 100000
            user_data['boosts'].append({'type': '10x', 'duration': 3})

        # Update user data in Firebase
        update_user(user_id, user_data)
        save_user_coins(user_id, user_data['coins'])
        return redirect(url_for('routes.boost'))

    return render_template('boost.html', user_data=user_data)


@routes.route('/airdrop')
def airdrop():
    return render_template('airdrop.html')
