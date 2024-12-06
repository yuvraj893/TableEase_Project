document.addEventListener("DOMContentLoaded", () => {
    const restaurantList = document.getElementById("restaurantList");
    const searchBar = document.getElementById("searchBar");

    // Mock data for now
    const restaurants = [
        { id: 1, name: "The Italian Place", cuisine: "Italian", location: "New York" },
        { id: 2, name: "Sushi World", cuisine: "Japanese", location: "Los Angeles" },
        { id: 3, name: "Burger Town", cuisine: "American", location: "Chicago" },
    ];

    const renderRestaurants = (filteredRestaurants) => {
        restaurantList.innerHTML = "";
        filteredRestaurants.forEach((restaurant) => {
            const card = document.createElement("div");
            card.className = "restaurant-card";
            card.innerHTML = `
                <h2>${restaurant.name}</h2>
                <p>Cuisine: ${restaurant.cuisine}</p>
                <p>Location: ${restaurant.location}</p>
                <button onclick="bookRestaurant(${restaurant.id})">Book Now</button>
            `;
            restaurantList.appendChild(card);
        });
    };

    searchBar.addEventListener("input", () => {
        const searchValue = searchBar.value.toLowerCase();
        const filtered = restaurants.filter(
            (r) =>
                r.name.toLowerCase().includes(searchValue) ||
                r.cuisine.toLowerCase().includes(searchValue)
        );
        renderRestaurants(filtered);
    });

    renderRestaurants(restaurants); // Initial render
});

function bookRestaurant(id) {
    alert(`Booking restaurant with ID: ${id}`);
    // Integration with POST /book endpoint will go here
}
