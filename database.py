import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection settings
DB_SETTINGS = {
    'database': 'yuvraj',  # Replace with your database name
    'user': 'yuvraj',      # Replace with your PostgreSQL username
    'password': '2003',    # Replace with your PostgreSQL password
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
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            conn.close()
            return user
        except Exception as e:
            print(f"Error during authentication: {e}")
            return None
    return None

# Function to fetch all restaurants
def get_all_restaurants():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM restaurants"
            cursor.execute(query)
            restaurants = cursor.fetchall()
            conn.close()
            return restaurants
        except Exception as e:
            print(f"Error fetching restaurants: {e}")
            return None
    return None

# Function to create a reservation
def create_reservation(user_id, restaurant_id, date, time, guests):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO reservations (userid, restaurantid, date, time, numberofguests, status)
                VALUES (%s, %s, %s, %s, %s, 'Pending')
            """
            cursor.execute(query, (user_id, restaurant_id, date, time, guests))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating reservation: {e}")
            return False
    return False

# Function to fetch reservations for a specific user
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

            # Convert time field to string format
            for reservation in reservations:
                reservation['time'] = reservation['time'].strftime('%H:%M:%S')  # Format as HH:MM:SS

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

            # Convert time field to string format
            for reservation in reservations:
                reservation['time'] = reservation['time'].strftime('%H:%M:%S')  # Format as HH:MM:SS

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

# Function to test the connection
def test_connection():
    conn = get_db_connection()
    if conn:
        print("Database connection successful!")
        conn.close()
    else:
        print("Database connection failed!")

if __name__ == '__main__':
    print("fetch_user_reservations is defined:", 'fetch_user_reservations' in globals())
    test_connection()
