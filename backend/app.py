from flask import Flask, request, jsonify, render_template, session, redirect
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
    fetch_user_notifications,
    update_reservation_status,
)

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
) 

app.secret_key = "2003"  

@app.route("/")
def home():
    return render_template("login.html")

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

@app.route("/restaurants_page", methods=["GET"])
def restaurants_page():
    user_id = session.get("user_id")  
    if not user_id:
        return redirect("/") 
    
    restaurants = get_all_restaurants()
    return render_template("restaurants.html", restaurants=restaurants, user_id=user_id)

@app.route("/book_page")
def book_page():
    restaurant_id = request.args.get("restaurant_id")  
    print(f"Restaurant ID from URL: {restaurant_id}")  

    restaurants = get_all_restaurants() 
    selected_restaurant = None

    if restaurant_id:
        try:
            selected_restaurant = next(
                (r for r in restaurants if str(r["restaurantid"]) == restaurant_id), None
            )
        except KeyError as e:
            print(f"KeyError: {e}. Check if 'restaurantid' field exists in restaurant records.")

    print(f"Selected Restaurant: {selected_restaurant}")  
    return render_template(
        "book.html",
        selected_restaurant=selected_restaurant,
        restaurants=restaurants,
    )

@app.route("/reservations_page")
def reservations_page():
    user_id = session.get("user_id") 
    if not user_id:
        return redirect("/") 
    
    reservations = fetch_user_reservations(user_id)  
    return render_template("reservations.html", reservations=reservations)

@app.route("/admin_reservations_page")
def admin_reservations_page():
    return render_template("admin_reservations.html")

@app.route("/customer_dashboard")
def customer_dashboard():
    return render_template("customer_dashboard.html")

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
            
            session['user_id'] = user_dict["id"]

            return jsonify({"message": "Login successful", "redirect": "/restaurants_page", "user": user_dict}), 200

        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@app.route("/restaurants", methods=["GET"])
def restaurants():
    restaurants = get_all_restaurants()
    if restaurants:
        return jsonify({"restaurants": restaurants}), 200
    return jsonify({"message": "Failed to fetch restaurants"}), 500

@app.route("/book", methods=["POST"])
def book():
    try:
        if request.content_type != "application/json":
            return jsonify({"message": "Content-Type must be application/json"}), 415

        data = request.json  
        user_id = session.get("user_id")  
        if not user_id:
            return jsonify({"message": "User is not logged in"}), 401

        restaurant_id = data.get("restaurant_id")
        date = data.get("date")
        time = data.get("time")
        guests = data.get("guests")

        if not all([restaurant_id, date, time, guests]):
            return jsonify({"message": "All fields are required"}), 400

        if create_reservation(user_id, restaurant_id, date, time, guests):
            return jsonify({"message": "Reservation successful", "redirect": "/reservations_page"}), 201

        return jsonify({"message": "Failed to create reservation"}), 500
    except Exception as e:
        print(f"Error in /book route: {e}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route("/reservations/<int:user_id>", methods=["GET"])
def get_reservations(user_id):
    try:
        reservations = fetch_user_reservations(user_id)
        if reservations:
            return jsonify({"reservations": reservations}), 200
        return jsonify({"message": "No reservations found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching reservations: {e}"}), 500

@app.route("/cancel/<int:reservation_id>", methods=["PUT"])
def cancel(reservation_id):
    try:
        if cancel_reservation(reservation_id):
            return jsonify({"message": "Reservation cancelled successfully"}), 200
        return jsonify({"message": "Failed to cancel reservation"}), 500
    except Exception as e:
        return jsonify({"message": f"Error cancelling reservation: {e}"}), 500

@app.route("/admin/reservations", methods=["GET"])
def admin_reservations():
    try:
        reservations = fetch_all_reservations()
        if reservations:
            return jsonify({"reservations": reservations}), 200
        return jsonify({"message": "No reservations found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching reservations: {e}"}), 500

@app.route("/update_status/<int:reservation_id>", methods=["PUT"])
def update_status(reservation_id):
    try:
        data = request.json
        new_status = data.get("status")  

        if not new_status:
            return jsonify({"message": "New status is required"}), 400

        if update_reservation_status(reservation_id, new_status):
            return jsonify({"message": f"Reservation status updated to {new_status}"}), 200
        return jsonify({"message": "Failed to update reservation status"}), 500
    except Exception as e:
        return jsonify({"message": f"Error updating reservation status: {e}"}), 500
    
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
    
@app.route("/reviews/<int:restaurant_id>")
def reviews_page(restaurant_id):
    try:
        reviews = fetch_reviews(restaurant_id)  
        return render_template("reviews.html", reviews=reviews, restaurant_id=restaurant_id)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

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

@app.route("/notifications", methods=["GET"])
def notifications_page():
    user_id = session.get("user_id")  
    if not user_id:
        return redirect("/") 

    notifications = fetch_user_notifications(user_id)
    return render_template("notifications.html", notifications=notifications)
    
@app.route("/logout", methods=["GET"])
def logout():
    session.pop('user_id', None)  
    return redirect("/")  

if __name__ == "__main__":
    app.run(debug=True)
