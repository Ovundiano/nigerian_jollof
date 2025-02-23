// Recipe-specific JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Recipe rating system
    const ratingStars = document.querySelectorAll('.rating-stars i');
    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            const recipeId = this.closest('.recipe-rating').dataset.recipeId;
            submitRating(recipeId, rating);
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
