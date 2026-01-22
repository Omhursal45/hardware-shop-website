document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("enquiryForm");

    form.addEventListener("submit", () => {
        const btn = form.querySelector(".submit-btn");
        btn.innerText = "Submitting...";
        btn.disabled = true;
    });
});
