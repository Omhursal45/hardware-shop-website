
    // Logic for Mobile Menu Toggle
    const menuBtn = document.getElementById('mobile-menu-btn');
    const navMenu = document.getElementById('nav-menu');

    menuBtn.addEventListener('click', (e) => {
        navMenu.classList.toggle('active');
        // Prevent click from bubbling up if you add a 'click outside to close' feature later
        e.stopPropagation();
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navMenu.contains(e.target) && !menuBtn.contains(e.target)) {
            navMenu.classList.remove('active');
        }
    });
