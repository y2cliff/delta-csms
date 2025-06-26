<script>
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => {
            alert.classList.add("fade");
            setTimeout(() => alert.remove(), 500); // Ensure element is removed after fading
        });
    }, 5000); // 5 seconds delay
});
</script>
