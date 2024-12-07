TableEase - Simplifying Restaurant Reservations

TableEase is a user-friendly web application designed to streamline the process of exploring restaurants, reading reviews, booking reservations, and managing notifications. Built using Flask and PostgreSQL, TableEase provides an intuitive interface and powerful backend capabilities to ensure a seamless user experience. Follow the user manual below to set up and use the application effectively.

User Manual for TableEase

1. Setting Up the Application

   Step 1: Clone the Repository  
   --> Open your terminal or command prompt.

   --> Navigate to the directory where you want to clone the repository.

   --> Run the following command:
   git clone https://github.com/yuvraj893/TableEase_Project.git

<img width="730" alt="Screenshot 2024-12-06 at 6 43 41 PM" src="https://github.com/user-attachments/assets/89be3a11-cd18-4917-9be6-669d815323fe">

Step 2: Set Up the Environment

--> Navigate into the project directory:

      cd <project-directory>

--> Install the required Python packages:

      pip install -r requirements.txt

<img width="1074" alt="Screenshot 2024-12-06 at 6 51 50 PM" src="https://github.com/user-attachments/assets/abb00fbf-69df-41e2-a82e-cacfe6dc435e">

--> Ensure PostgreSQL is installed and running on your machine.

--> Set up the database:

Create a new database (e.g., tableease_db).

Run the provided SQL script to create tables and populate initial data:

    psql -U <username> -d <database-name> setup.sql

Replace <username> with your PostgreSQL username and <database-name> with your database name.

<img width="817" alt="Screenshot 2024-12-06 at 7 00 13 PM" src="https://github.com/user-attachments/assets/ac24ac52-6dc4-433f-b9ac-cf28ca2fb5d7">

Step 3: Run the Application

--> Start the Flask application:

    python backend/app.py


--> Open your web browser and navigate to:

    http://127.0.0.1:5000

<img width="896" alt="Screenshot 2024-12-06 at 7 03 16 PM" src="https://github.com/user-attachments/assets/80aed3b2-38df-4213-abd0-6be7240472a4">

2. Using the Application

   Step 1: View Available Restaurants

   --> On the homepage, you'll see a list of restaurants.

   --> Use the Search bar to filter restaurants by name, location, or cuisine.

   --> Each restaurant card shows the name, location, and cuisine.

<img width="628" alt="Screenshot 2024-12-06 at 7 05 39 PM" src="https://github.com/user-attachments/assets/e16331ed-cc5a-4819-94f5-01264bcc040e">

Step 2: View Reviews for a Restaurant

--> Next to each restaurant, click the View Reviews button to see reviews for that restaurant.

--> The reviews page will display user feedback for the selected restaurant.

<img width="715" alt="Screenshot 2024-12-06 at 7 06 52 PM" src="https://github.com/user-attachments/assets/9c050ab5-579a-4917-a3cc-3343868ab897">

Step 3: Book a Reservation

--> Click the Book a Reservation button for a restaurant.

--> Fill in the following details:

Date: Select the reservation date.

Time: Enter the reservation time.

Number of Guests: Specify the number of guests.

--> Click Book Now to confirm your reservation.

<img width="816" alt="Screenshot 2024-12-06 at 7 08 46 PM" src="https://github.com/user-attachments/assets/b8ebc74a-00a4-427f-bf7d-7e141715c369">

Step 4: Check Notifications

--> Click the Notifications button on the homepage.

--> You'll see a list of notifications related to your reservations (e.g., confirmations, cancellations).

Step 5: Logout

--> To log out of the application, click the Logout button at the bottom of the homepage.

--> This will securely log you out and redirect you to the login page (if implemented).

<img width="620" alt="Screenshot 2024-12-06 at 7 12 33 PM" src="https://github.com/user-attachments/assets/ec360419-caaa-4e42-b3e8-4e6d77e2e4b4">

3. Troubleshooting

   Issue: Application Not Running

   --> Ensure the Flask server is running. Check the terminal for errors.

   --> Ensure the database is correctly set up and running.

   Issue: Buttons Not Working

   --> Refresh the page in your browser.

   --> Check the terminal for errors or logs.

4. Contact Support

   --> If you face any issues not covered in this guide, please contact:

   Email: ybhatia1@asu.edu
