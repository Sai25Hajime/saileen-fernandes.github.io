document.addEventListener("DOMContentLoaded", function() {
    const questions = document.querySelectorAll(".faq-question");
    const darkModeToggle = document.createElement("button");

    // Add Dark Mode Toggle Button
    darkModeToggle.textContent = "Toggle Dark Mode";
    darkModeToggle.style.position = "fixed";
    darkModeToggle.style.top = "10px";
    darkModeToggle.style.right = "10px";
    darkModeToggle.style.width = "150px"; /* Fix button width */
    darkModeToggle.style.height = "40px"; /* Fix button height */
    darkModeToggle.style.padding = "5px 10px";
    darkModeToggle.style.backgroundColor = "#d1478d";
    darkModeToggle.style.color = "white";
    darkModeToggle.style.border = "none";
    darkModeToggle.style.borderRadius = "5px";
    darkModeToggle.style.cursor = "pointer";
    darkModeToggle.style.zIndex = "1000"; /* Ensure it's above other elements */
    document.body.appendChild(darkModeToggle);

    questions.forEach(question => {
        question.addEventListener("click", function() {
            const answer = this.nextElementSibling;
            const isActive = answer.style.display === "block";

            document.querySelectorAll(".faq-answer").forEach(ans => ans.style.display = "none");

            if (!isActive) {
                answer.style.display = "block";
            }
        });
    });
    // Dark Mode Functionality
    darkModeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });

    // Load theme from localStorage
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});
