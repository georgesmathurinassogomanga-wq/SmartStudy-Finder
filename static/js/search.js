document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function () {
            const input = form.querySelector("input[name='q']").value;

            if (!input.trim()) {
                alert("Entre un sujet valide !");
            }
        });
    }

});