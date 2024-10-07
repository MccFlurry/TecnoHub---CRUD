document.addEventListener('DOMContentLoaded', function() {
    // Add any JavaScript functionality for the admin panel here
    console.log('Admin panel loaded');

    // Example: Toggle mobile menu
    const menuButton = document.querySelector('#mobile-menu-button');
    const sidebar = document.querySelector('#sidebar');

    if (menuButton && sidebar) {
        menuButton.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
        });
    }

});