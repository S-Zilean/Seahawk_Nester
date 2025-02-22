document.addEventListener("DOMContentLoaded", function() {
    const fetchLinks = document.querySelectorAll(".fetch-link");
    fetchLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const url = this.getAttribute("href");
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    document.getElementById("content").innerHTML = html;
                })
                .catch(error => console.warn('Something went wrong.', error));
        });
    });

    document.getElementById('harvesters-toggle').addEventListener('click', function(event) {
        event.preventDefault();
        var submenu = document.getElementById('harvesters-menu');
        submenu.classList.toggle('active');
        var icon = this.querySelector('.dropdown-icon');
        icon.classList.toggle('active');
    });

    document.getElementById('admin-tools-toggle').addEventListener('click', function(event) {
        event.preventDefault();
        var submenu = document.getElementById('admin-tools-menu');
        submenu.classList.toggle('active');
        var icon = this.querySelector('.dropdown-icon');
        icon.classList.toggle('active');
    });

    // Assurez-vous que les liens dans les sous-menus ne sont pas empêchés par le JavaScript
    document.querySelectorAll('.submenu a').forEach(function(link) {
        link.addEventListener('click', function(event) {
            // Ne pas empêcher la redirection des liens dans les sous-menus
            event.stopPropagation();
        });
    });
});