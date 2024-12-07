document.addEventListener("DOMContentLoaded", () => {
    const bookNowButton = document.querySelector("#bookNowButton");

    bookNowButton.addEventListener("click", async (event) => {
        event.preventDefault(); 
        const restaurantId = document.querySelector("#restaurantSelect").value;
        const date = document.querySelector("#dateInput").value;
        const time = document.querySelector("#timeInput").value;
        const guests = document.querySelector("#guestsInput").value;

        try {
            const response = await fetch("/book", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", 
                },
                body: JSON.stringify({
                    restaurant_id: restaurantId,
                    date: date,
                    time: time,
                    guests: guests,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                window.location.href = data.redirect; 
            } else {
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Failed to book the reservation. Please try again.");
        }
    });
});
