document.querySelectorAll("[id^='toggle_']").forEach((toggleIcon) => {
    toggleIcon.addEventListener("click", function () {
        const passwordField = document.getElementById(toggleIcon.id.replace("toggle_", "id_"));
        const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
        passwordField.setAttribute("type", type);
        this.classList.toggle("bi-eye");
        this.classList.toggle("bi-eye-slash");
    });
});