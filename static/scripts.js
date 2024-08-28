document.addEventListener('DOMContentLoaded', function () {
    // Example of adding hover effects dynamically
    const cards = document.querySelectorAll('.dashboard-card');

    cards.forEach(card => {
        card.addEventListener('mouseover', function () {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0px 10px 20px rgba(0, 0, 0, 0.2)';
        });

        card.addEventListener('mouseout', function () {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0px 0px 15px rgba(0, 0, 0, 0.1)';
        });
    });

    // You can add more interactivity here
});
