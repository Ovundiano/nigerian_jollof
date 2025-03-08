/* jshint esversion: 6 */
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to elements with fade-in class
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.style.opacity = '0';
    });

    // Intersection Observer for fade-in elements
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transition = 'opacity 0.5s ease-in';
            }
        });
    });

    fadeElements.forEach(element => {
        fadeObserver.observe(element);
    });

    // Smooth transitions for social media links
    const socialLinks = document.querySelectorAll('.social-links a');
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add loading animation for images
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });
        if (img.dataset.src) {
            img.src = img.dataset.src;
        }
    });
});
