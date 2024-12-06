from flask import Flask, request, jsonify, render_template
from database import (
    authenticate_user,
    create_user,
    get_all_restaurants,
    create_reservation,
    fetch_user_reservations,
    cancel_reservation,
    fetch_all_reservations,
    fetch_reviews,
    add_review,
    update_reservation_status,
)

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)

# Route to render the home (login) page
@app.route("/")
def home():
    return render_template("login.html")

# Route to render the signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        data = request.json
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if email and password and name:
            result = create_user(email, password, name)
            if result["success"]:
                return jsonify({"message": result["message"]}), 201
            else:
                return jsonify({"message": result["message"]}), 400
        return jsonify({"message": "Invalid input data."}), 400

# Route to render the restaurants page
@app.route("/restaurants_page", methods=["GET"])
def restaurants_page():
    search_query = request.args.get("search", "")
    if search_query:
        # Filter restaurants based on the search query
        restaurants = [
            r for r in get_all_restaurants()
            if search_query.lower() in r["name"].lower()
            or search_query.lower() in r["location"].lower()
            or search_query.lower() in r["cuisine"].lower()
        ]
    else:
        restaurants = get_all_restaurants()
    
    return render_template("restaurants.html", restaurants=restaurants)

# Route to render the booking page
@app.route("/book_page")
def book_page():
    restaurant_id = request.args.get("restaurant_id")
    print(f"Restaurant ID from URL: {restaurant_id}")  # Debug log

    restaurants = get_all_restaurants()
    selected_restaurant = None

    if restaurant_id:
        try:
            selected_restaurant = next(
                (r for r in restaurants if str(r["id"]) == restaurant_id), None
            )
        except KeyError as e:
            print(f"KeyError: {e}. Check if 'id' field exists in restaurant records.")
    
    print(f"Selected Restaurant: {selected_restaurant}")  # Debug log
    return render_template(
        "book.html",
        selected_restaurant=selected_restaurant,
        restaurants=restaurants,
    )

# Route to render the user reservations page
@app.route("/reservations_page")
def reservations_page():
    return render_template("reservations.html")

# Route to render the admin reservations page
@app.route("/admin_reservations_page")
def admin_reservations_page():
    return render_template("admin_reservations.html")

# Route for Customer Dashboard
@app.route("/customer_dashboard")
def customer_dashboard():
    return render_template("customer_dashboard.html")

# API Route for user login
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        user = authenticate_user(email, password)

        if user:
            if isinstance(user, tuple):
                user_dict = {
                    "id": user[0],
                    "name": user[1],
                    "role": user[2],
                }
            else:
                user_dict = user
            return jsonify({"message": "Login successful", "redirect": "/restaurants_page", "user": user_dict}), 200

        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# API Route to fetch all restaurants
@app.route("/restaurants", methods=["GET"])
def restaurants():
    restaurants = get_all_restaurants()
    if restaurants:
        return jsonify({"restaurants": restaurants}), 200
    return jsonify({"message": "Failed to fetch restaurants"}), 500

# API Route to book a reservation
@app.route("/book", methods=["POST"])
def book():
    try:
        data = request.json
        print("Incoming reservation data:", data)  # Debug log

        user_id = data.get("user_id")
        restaurant_id = data.get("restaurant_id")
        date = data.get("date")
        time = data.get("time")
        guests = data.get("guests")

        if not restaurant_id:
            return jsonify({"message": "Restaurant ID is required"}), 400

        if create_reservation(user_id, restaurant_id, date, time, guests):
            return jsonify({"message": "Reservation successful"}), 201

        return jsonify({"message": "Failed to create reservation"}), 500
    except Exception as e:
        print(f"Error in /book route: {e}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

# API Route to fetch reservations for a user
@app.route("/reservations/<int:user_id>", methods=["GET"])
def get_reservations(user_id):
    try:
        reservations = fetch_user_reservations(user_id)
        if reservations:
            return jsonify({"reservations": reservations}), 200
        return jsonify({"message": "No reservations found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching reservations: {e}"}), 500

# API Route to cancel a reservation
@app.route("/cancel/<int:reservation_id>", methods=["PUT"])
def cancel(reservation_id):
    try:
        if cancel_reservation(reservation_id):
            return jsonify({"message": "Reservation cancelled successfully"}), 200
        return jsonify({"message": "Failed to cancel reservation"}), 500
    except Exception as e:
        return jsonify({"message": f"Error cancelling reservation: {e}"}), 500

# API Route for admin to fetch all reservations
@app.route("/admin/reservations", methods=["GET"])
def admin_reservations():
    try:
        reservations = fetch_all_reservations()
        if reservations:
            return jsonify({"reservations": reservations}), 200
        return jsonify({"message": "No reservations found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching reservations: {e}"}), 500

# API Route to update the status of a reservation
@app.route("/update_status/<int:reservation_id>", methods=["PUT"])
def update_status(reservation_id):
    try:
        data = request.json
        new_status = data.get("status")  # Example: 'Confirmed', 'Denied', etc.

        if not new_status:
            return jsonify({"message": "New status is required"}), 400

        if update_reservation_status(reservation_id, new_status):
            return jsonify({"message": f"Reservation status updated to {new_status}"}), 200
        return jsonify({"message": "Failed to update reservation status"}), 500
    except Exception as e:
        return jsonify({"message": f"Error updating reservation status: {e}"}), 500
    
# Route to fetch and display reviews for a restaurant
@app.route("/review", methods=["POST"])
def review():
    try:
        data = request.json
        user_id = data.get("user_id")
        restaurant_id = data.get("restaurant_id")
        comment = data.get("comment")
        rating = data.get("rating")

        if add_review(user_id, restaurant_id, comment, rating):
            return jsonify({"message": "Review added successfully"}), 201
        else:
            return jsonify({"message": "Failed to add review"}), 500
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500
    
# Route to fetch and display reviews for a restaurant
@app.route("/reviews/<int:restaurant_id>")
def reviews_page(restaurant_id):
    try:
        reviews = fetch_reviews(restaurant_id)  # Fetch reviews for the restaurant
        return render_template("reviews.html", reviews=reviews, restaurant_id=restaurant_id)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

# API route to submit a review
@app.route("/add_review", methods=["POST"])
def add_review_route():
    try:
        data = request.json
        user_id = data.get("user_id")
        restaurant_id = data.get("restaurant_id")
        comment = data.get("comment")
        rating = data.get("rating")

        if add_review(user_id, restaurant_id, comment, rating):
            return jsonify({"message": "Review added successfully"}), 201
        else:
            return jsonify({"message": "Failed to add review"}), 500
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
