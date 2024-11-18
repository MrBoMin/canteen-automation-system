fetch('header.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('header-placeholder').innerHTML = data;
    })
    .catch(error => console.error('Error loading the header:', error));
fetch('footer.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer-placeholder').innerHTML = data;
    })
    .catch(error => console.error('Error loading the header:', error));

// Carousel navigation functionality
document.querySelectorAll('.carousel-nav').forEach(button => {
    button.addEventListener('click', () => {
        const container = document.querySelector('.discounts-container');
        const scrollAmount = button.classList.contains('left') ? -220 : 220;
        container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("toggleButton");
    const closeButton = document.getElementById("closeButton");
    const sideContainer = document.getElementById("sideContainer");
    const overlay = document.getElementById("overlay");

    // Show side-container and overlay on toggleButton click
    toggleButton.addEventListener("click", function() {
        sideContainer.classList.add("active");
        overlay.classList.add("active");
    });

    // Hide side-container and overlay on closeButton or overlay click
    closeButton.addEventListener("click", function() {
        sideContainer.classList.remove("active");
        overlay.classList.remove("active");
    });

    overlay.addEventListener("click", function() {
        sideContainer.classList.remove("active");
        overlay.classList.remove("active");
    });
});



    