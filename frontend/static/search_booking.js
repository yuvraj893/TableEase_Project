document.getElementById("bookingForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const user_id = 1; 
    const restaurant_id = document.getElementById("restaurant").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;
    const guests = document.getElementById("guests").value;

    if (!restaurant_id) {
        alert("Please select a restaurant.");
        return;
    }

    const reservationData = {
        user_id,
        restaurant_id,
        date,
        time,
        guests,
    };

    try {
        const response = await fetch("/book", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(reservationData),
        });

        if (response.ok) {
            alert("Reservation successful!");
            location.href = "/reservations_page";
        } else {
            alert("Failed to create reservation.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});
