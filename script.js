document.addEventListener("DOMContentLoaded", function() {
    const questions = document.querySelectorAll(".faq-question");

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
});
