import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt  

DB_SETTINGS = {
    'database': 'yuvraj',  
    'user': 'yuvraj',      
    'password': '2003',    
    'host': 'localhost',
    'port': '5432'
}

# Function to connect to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            database=DB_SETTINGS['database'],
            user=DB_SETTINGS['user'],
            password=DB_SETTINGS['password'],
            host=DB_SETTINGS['host'],
            port=DB_SETTINGS['port']
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to authenticate user
def authenticate_user(email, password):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):  
                return user
            return None
        except Exception as e:
            print(f"Error during authentication: {e}")
            return None
    return None

# Function to fetch all restaurants
def get_all_restaurants(query=None):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if query:
                query = f"%{query}%"
                sql = """
                    SELECT restaurantid, name, location, cuisine
                    FROM restaurants
                    WHERE name ILIKE %s OR location ILIKE %s OR cuisine ILIKE %s
                """
                cursor.execute(sql, (query, query, query))
            else:
                sql = "SELECT restaurantid, name, location, cuisine FROM restaurants"
                cursor.execute(sql)
            restaurants = cursor.fetchall()
            conn.close()
            return restaurants
        except Exception as e:
            print(f"Error fetching restaurants: {e}")
            return None
    return None


def create_reservation(user_id, restaurant_id, date, time, guests):
    try:
        user_id = int(user_id)  
        restaurant_id = int(restaurant_id)  
        guests = int(guests)  

        conn = get_db_connection()
        query = """
            INSERT INTO reservations (userid, restaurantid, date, time, numberofguests, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id, restaurant_id, date, time, guests))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating reservation: {e}")
        return False

def fetch_user_reservations(user_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT r.reservationid, r.date, r.time, r.numberofguests, r.status, res.name AS restaurant_name
                FROM reservations r
                JOIN restaurants res ON r.restaurantid = res.restaurantid
                WHERE r.userid = %s
                ORDER BY r.date, r.time
            """
            cursor.execute(query, (user_id,))
            reservations = cursor.fetchall()

            for reservation in reservations:
                reservation['time'] = reservation['time'].strftime('%H:%M:%S')  

            conn.close()
            return reservations
        except Exception as e:
            print(f"Error fetching reservations: {e}")
            return None
    return None

# Function to fetch all reservations (Admin)
def fetch_all_reservations():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT r.reservationid, r.date, r.time, r.numberofguests, r.status, res.name AS restaurant_name, u.name AS user_name
                FROM reservations r
                JOIN restaurants res ON r.restaurantid = res.restaurantid
                JOIN users u ON r.userid = u.userid
                ORDER BY r.date, r.time
            """
            cursor.execute(query)
            reservations = cursor.fetchall()

            for reservation in reservations:
                reservation['time'] = reservation['time'].strftime('%H:%M:%S')  

            conn.close()
            return reservations
        except Exception as e:
            print(f"Error fetching all reservations: {e}")
            return None
    return None

# Function to cancel a reservation
def cancel_reservation(reservation_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE reservations
                SET status = 'Cancelled'
                WHERE reservationid = %s
            """
            cursor.execute(query, (reservation_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error cancelling reservation: {e}")
            return False
    return False

# Function to update the status of a reservation
def update_reservation_status(reservation_id, new_status):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE reservations
                SET status = %s
                WHERE reservationid = %s
            """
            cursor.execute(query, (new_status, reservation_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating reservation status: {e}")
            return False
    return False

# Function to create a new user
def create_user(email, password, name):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            check_query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(check_query, (email,))
            if cursor.fetchone():
                conn.close()
                return {"success": False, "message": "Email already exists"}

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            insert_query = """
            INSERT INTO users (email, password, name)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (email, hashed_password, name))
            conn.commit()
            conn.close()
            return {"success": True, "message": "User created successfully"}
        except Exception as e:
            print(f"Error creating user: {e}")
            return {"success": False, "message": "Error creating user"}
    return {"success": False, "message": "Database connection failed"}

def fetch_reviews(restaurant_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT r.reviewid, r.userid, u.name AS user_name, r.comment, r.rating, r.timestamp
                FROM reviews r
                JOIN users u ON r.userid = u.userid
                WHERE r.restaurantid = %s
                ORDER BY r.timestamp DESC
            """
            cursor.execute(query, (restaurant_id,))
            reviews = cursor.fetchall()
            conn.close()
            return reviews
        except Exception as e:
            print(f"Error fetching reviews: {e}")
            return None
    return None

def add_review(user_id, restaurant_id, comment, rating):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO reviews (userid, restaurantid, comment, rating, timestamp)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(query, (user_id, restaurant_id, comment, rating))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding review: {e}")
            return False
    return False

def fetch_user_notifications(user_id):
    try:
        conn = get_db_connection()
        if not conn:
            raise Exception("Failed to establish database connection.")
        
        cursor = conn.cursor()

        query = """
        SELECT notificationid, userid, message, date, type
        FROM notifications
        WHERE userid = %s
        ORDER BY date DESC;
        """
        cursor.execute(query, (user_id,))
        notifications = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            {
                "notificationid": row[0],
                "userid": row[1],
                "message": row[2],
                "date": row[3],
                "type": row[4],
            }
            for row in notifications
        ]
    except Exception as e:
        print(f"Error fetching notifications: {e}")
        return []

def test_connection():
    conn = get_db_connection()
    if conn:
        print("Database connection successful!")
        conn.close()
    else:
        print("Database connection failed!")

if __name__ == "__main__":
    conn = get_db_connection()
    print("Connected to the database successfully!")
    conn.close()