document.addEventListener("DOMContentLoaded", async () => {
    const notificationsList = document.getElementById("notificationsList");

    try {
        const response = await fetch('/notifications?format=json');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();

        if (data.notifications && data.notifications.length > 0) {
            data.notifications.forEach(notification => {
                const card = document.createElement("div");
                card.className = `notification-card ${notification.type.toLowerCase()}`; 

                card.innerHTML = `
                    <div class="notification-type">${capitalize(notification.type)}</div>
                    <div class="notification-message">${notification.message}</div>
                    <div class="notification-date">${new Date(notification.date).toLocaleString()}</div>
                `;

                notificationsList.appendChild(card);
            });
        } else {
            notificationsList.innerHTML = `<p>No notifications available.</p>`;
        }
    } catch (error) {
        console.error("Error fetching notifications:", error);
        notificationsList.innerHTML = `<p>Failed to load notifications. Please try again later.</p>`;
    }
});

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}
