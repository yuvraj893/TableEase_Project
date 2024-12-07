document.addEventListener("DOMContentLoaded", async () => {
    const reviewsList = document.getElementById("reviewsList");
    const reviewForm = document.getElementById("reviewForm");

    // Get restaurant ID dynamically from the hidden input field
    const restaurantId = document.getElementById("restaurantId").value;

    // Function to fetch and display reviews
    const loadReviews = async () => {
        reviewsList.innerHTML = ""; // Clear existing reviews
        try {
            const response = await fetch(`/reviews/${restaurantId}`);
            const data = await response.json();

            // Render reviews
            data.reviews.forEach(review => {
                const card = document.createElement("div");
                card.className = "review-card";
                card.innerHTML = `
                    <div class="rating">Rating: ${review.rating}/5</div>
                    <p><strong>${review.user_name}</strong> (${new Date(review.timestamp).toLocaleString()})</p>
                    <p>${review.comment}</p>
                `;
                reviewsList.appendChild(card);
            });
        } catch (error) {
            console.error("Error fetching reviews:", error);
            reviewsList.innerHTML = `<p>Failed to load reviews. Please try again later.</p>`;
        }
    };

    // Load reviews on page load
    await loadReviews();

    // Handle review form submission
    reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const rating = document.getElementById("rating").value;
        const comment = document.getElementById("comment").value;


        try {
            const response = await fetch('/review', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    restaurant_id: restaurantId, 
                    comment: comment, 
                    rating: rating 
                })
            });            

            if (response.ok) {
                alert("Review submitted successfully!");
                await loadReviews(); // Reload reviews without refreshing the page
                reviewForm.reset(); // Clear the form inputs
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
