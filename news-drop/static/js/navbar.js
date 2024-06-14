// static/js/sidebar.js

document.addEventListener("DOMContentLoaded", function() {
    var addDropButton = document.getElementById("addDropButton");
    var dropsList = document.getElementById("dropsList");

    addDropButton.addEventListener("click", function(event) {
        event.preventDefault();

        var newDrop = document.createElement("li");
        newDrop.className = "nav-item";
        newDrop.innerHTML = `
            <a class="nav-link d-flex align-items-center gap-2" href="#">
                <svg class="bi"><use xlink:href="#file-earmark-text"/></svg>
                Madrid
            </a>
        `;

        dropsList.appendChild(newDrop);
    });
});
