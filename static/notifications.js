document.addEventListener("DOMContentLoaded", async () => {
    const notificationsList = document.getElementById("notificationsList");

    try {
        // Fetch notifications data from the backend
        const response = await fetch('/notifications');
        const data = await response.json();

        // Render notifications on the page
        data.notifications.forEach(notification => {
            const card = document.createElement("div");
            card.className = "notification-card";

            card.innerHTML = `
                <div class="notification-type">${notification.type}</div>
                <div class="notification-message">${notification.message}</div>
                <div class="notification-date">${new Date(notification.date).toLocaleDateString()}</div>
            `;

            notificationsList.appendChild(card);
        });
    } catch (error) {
        console.error("Error fetching notifications:", error);
        notificationsList.innerHTML = `<p>Failed to load notifications. Please try again later.</p>`;
    }
});
