document.addEventListener('DOMContentLoaded', function () {

    var toggle = document.getElementById('mobileToggle');
    var navLinks = document.getElementById('navLinks');

    if (toggle && navLinks) {
        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            var isOpen = navLinks.classList.contains('active');
            navLinks.classList.toggle('active', !isOpen);
            toggle.classList.toggle('active', !isOpen);
            toggle.setAttribute('aria-expanded', String(!isOpen));
        });

        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navLinks.classList.remove('active');
                toggle.classList.remove('active');
                toggle.setAttribute('aria-expanded', 'false');
            });
        });

        document.addEventListener('click', function (e) {
            if (
                navLinks.classList.contains('active') &&
                !navLinks.contains(e.target) &&
                !toggle.contains(e.target)
            ) {
                navLinks.classList.remove('active');
                toggle.classList.remove('active');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Navbar shadow on scroll
    var navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            navbar.style.boxShadow = window.pageYOffset > 100
                ? '0 2px 16px rgba(0,0,0,0.1)'
                : 'none';
        });
    }

    // Gallery hover
    document.querySelectorAll('.gallery-item').forEach(function (item) {
        item.addEventListener('mouseenter', function () { this.style.zIndex = '10'; });
        item.addEventListener('mouseleave', function () { this.style.zIndex = '1'; });
    });

    window.scrollTo(0, 0);
});