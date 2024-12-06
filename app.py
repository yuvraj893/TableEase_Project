from flask import Flask, request, jsonify
from database import (
    authenticate_user,
    get_all_restaurants,
    create_reservation,
    fetch_user_reservations,
    cancel_reservation,
    fetch_all_reservations,
    update_reservation_status
)

app = Flask(__name__)

# Basic route for testing
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to TableEase Backend!'})

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = authenticate_user(email, password)
    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Route to fetch all restaurants
@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants = get_all_restaurants()
    if restaurants:
        return jsonify({'restaurants': restaurants}), 200
    return jsonify({'message': 'Failed to fetch restaurants'}), 500

# Route to book a reservation
@app.route('/book', methods=['POST'])
def book():
    data = request.json
    user_id = data.get('user_id')
    restaurant_id = data.get('restaurant_id')
    date = data.get('date')
    time = data.get('time')
    guests = data.get('guests')

    if create_reservation(user_id, restaurant_id, date, time, guests):
        return jsonify({'message': 'Reservation successful'}), 201
    return jsonify({'message': 'Failed to create reservation'}), 500

# Route to fetch reservations for a user
@app.route('/reservations/<int:user_id>', methods=['GET'])
def get_reservations(user_id):
    try:
        reservations = fetch_user_reservations(user_id)
        if reservations:
            return jsonify({'reservations': reservations}), 200
        return jsonify({'message': 'No reservations found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error fetching reservations: {e}'}), 500

# Route to cancel a reservation
@app.route('/cancel/<int:reservation_id>', methods=['PUT'])
def cancel(reservation_id):
    try:
        if cancel_reservation(reservation_id):
            return jsonify({'message': 'Reservation cancelled successfully'}), 200
        return jsonify({'message': 'Failed to cancel reservation'}), 500
    except Exception as e:
        return jsonify({'message': f'Error cancelling reservation: {e}'}), 500

# Route for admin to fetch all reservations
@app.route('/admin/reservations', methods=['GET'])
def admin_reservations():
    try:
        reservations = fetch_all_reservations()
        if reservations:
            return jsonify({'reservations': reservations}), 200
        return jsonify({'message': 'No reservations found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error fetching reservations: {e}'}), 500

# Route to update the status of a reservation
@app.route('/update_status/<int:reservation_id>', methods=['PUT'])
def update_status(reservation_id):
    try:
        data = request.json
        new_status = data.get('status')  # Example: 'Confirmed', 'Denied', etc.

        if not new_status:
            return jsonify({'message': 'New status is required'}), 400

        if update_reservation_status(reservation_id, new_status):
            return jsonify({'message': f'Reservation status updated to {new_status}'}), 200
        return jsonify({'message': 'Failed to update reservation status'}), 500
    except Exception as e:
        return jsonify({'message': f'Error updating reservation status: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
