/* jshint esversion: 8 */
// Recipe-specific JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Original Recipe rating system for recipe cards
    const ratingStars = document.querySelectorAll('.rating-stars i');
    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            const recipeId = this.closest('.recipe-rating').dataset.recipeId;
            submitRating(recipeId, rating);
        });
    });

    // Enhanced rating system for recipe detail page
    const ratingInputs = document.querySelectorAll('.rating-input input[type="radio"]');
    const ratingLabels = document.querySelectorAll('.rating-input label');
    
    // Pre-select the user's existing rating if available
    const userRatingElement = document.getElementById('user-rating-value');
    if (userRatingElement) {
        const userRating = parseInt(userRatingElement.value);
        if (!isNaN(userRating) && userRating >= 1 && userRating <= 5) {
            document.getElementById(`id_value_${userRating}`).checked = true;
            highlightStars(userRating);
        }
    }
    
    // Add click event listeners to all rating inputs
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            const value = parseInt(this.value);
            highlightStars(value);
        });
    });
    
    // Function to highlight stars based on selected value
    function highlightStars(value) {
        ratingLabels.forEach((label, index) => {
            // Convert NodeList indices (0-based) to rating values (1-based)
            const starValue = index + 1;
            
            if (starValue <= value) {
                label.style.color = '#ffc107'; // Highlighted color (same as in your CSS)
            } else {
                label.style.color = '#dddddd'; // Default color
            }
        });
    }
    
    // Fix for hover effect after selection
    const ratingOptions = document.querySelectorAll('.rating-option');
    
    ratingOptions.forEach(option => {
        option.addEventListener('mouseenter', function() {
            // Don't override hover effect with selection
            // This allows proper hover behavior
        });
        
        option.addEventListener('mouseleave', function() {
            // Restore selection highlight when mouse leaves
            const checkedInput = document.querySelector('.rating-input input[type="radio"]:checked');
            if (checkedInput) {
                const value = parseInt(checkedInput.value);
                highlightStars(value);
            } else {
                // If no selection, reset all stars
                ratingLabels.forEach(label => {
                    label.style.color = '#dddddd';
                });
            }
        });
    });

    // Recipe search functionality
    const searchForm = document.querySelector('.recipe-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchInput = this.querySelector('input[type="search"]');
            if (searchInput.value.trim()) {
                this.submit();
            }
        });
    }

    // Recipe card hover effects
    const recipeCards = document.querySelectorAll('.recipe-card');
    recipeCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover');
        });
    });

    // Helper function to submit rating
    async function submitRating(recipeId, rating) {
        try {
            const response = await fetch('/recipes/rate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    recipe_id: recipeId,
                    rating: rating
                })
            });
            if (response.ok) {
                updateRatingDisplay(recipeId, rating);
            }
        } catch (error) {
            console.error('Error submitting rating:', error);
        }
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Helper function to update rating display
    function updateRatingDisplay(recipeId, rating) {
        const ratingContainer = document.querySelector(`[data-recipe-id="${recipeId}"]`);
        if (ratingContainer) {
            const stars = ratingContainer.querySelectorAll('i');
            stars.forEach((star, index) => {
                if (index < rating) {
                    star.classList.remove('far');
                    star.classList.add('fas');
                } else {
                    star.classList.remove('fas');
                    star.classList.add('far');
                }
            });
        }
    }
});
