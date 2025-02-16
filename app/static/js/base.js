document.addEventListener("DOMContentLoaded", function() {
    const links = document.querySelectorAll(".sidebar a");
    links.forEach(link => {
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
});