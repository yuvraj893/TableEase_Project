document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/reservations/1"); 
        if (response.ok) {
            const data = await response.json();
            const reservationsBody = document.getElementById("reservations-body");

            data.reservations.forEach(reservation => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${reservation.restaurant_name}</td>
                    <td>${reservation.date}</td>
                    <td>${reservation.time}</td>
                    <td>${reservation.guests}</td>
                    <td>${reservation.status}</td>
                `;

                reservationsBody.appendChild(row);
            });
        } else {
            alert("Failed to fetch reservations.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Please try again later.");
    }
});
