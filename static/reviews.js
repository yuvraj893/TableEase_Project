document.addEventListener("DOMContentLoaded", async () => {
    const reviewsList = document.getElementById("reviewsList");
    const reviewForm = document.getElementById("reviewForm");

    const restaurantId = 1; // Replace with actual restaurant ID if dynamic

    try {
        // Fetch reviews for the restaurant
        const response = await fetch(`/reviews?restaurant_id=${restaurantId}`);
        const data = await response.json();

        // Render reviews on the page
        data.reviews.forEach(review => {
            const card = document.createElement("div");
            card.className = "review-card";
            card.innerHTML = `
                <div class="rating">Rating: ${review.rating}/5</div>
                <p>${review.comment}</p>
            `;
            reviewsList.appendChild(card);
        });
    } catch (error) {
        console.error("Error fetching reviews:", error);
        reviewsList.innerHTML = `<p>Failed to load reviews. Please try again later.</p>`;
    }

    // Handle review form submission
    reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const rating = document.getElementById("rating").value;
        const comment = document.getElementById("comment").value;

        try {
            const response = await fetch('/review', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ restaurant_id: restaurantId, rating, comment })
            });

            if (response.ok) {
                alert("Review submitted successfully!");
                location.reload(); // Reload the page to fetch new reviews
            } else {
                const errorData = await response.json();
                alert("Failed to submit review: " + errorData.message);
            }
        } catch (error) {
            console.error("Error submitting review:", error);
            alert("Something went wrong. Please try again.");
        }
    });
});
