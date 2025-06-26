// function updateSelect2Theme() {
//     $(".select2-container").each(function () {
//         $(this).toggleClass("dark-mode", document.documentElement.classList.contains("dark-mode"));
//     });

//     $(".select2-dropdown").each(function () {
//         $(this).toggleClass("dark-mode", document.documentElement.classList.contains("dark-mode"));
//     });
// }


document.addEventListener("DOMContentLoaded", function () {
    const html = document.documentElement;
    const darkModeToggle = document.getElementById("dark-mode-toggle");
    // const tables = document.querySelectorAll("table");
    // const select2Fields = document.querySelectorAll(".select2-container");

    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.classList.toggle("dark-mode", savedTheme === "dark");
    html.setAttribute("data-bs-theme", savedTheme);
    // document.body.setAttribute("data-bs-theme", savedTheme);
    // tables.forEach(table => table.classList.toggle("dark-mode", savedTheme === "dark"));
    // select2Fields.forEach(field => field.classList.toggle("dark-mode", savedTheme === "dark"));

    // updateSelect2Theme(); // Apply theme changes to Select2 on load

    darkModeToggle.innerHTML = savedTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";

    // Toggle dark mode on button click
    darkModeToggle.addEventListener("click", function () {
        const newTheme = document.documentElement.classList.contains("dark-mode") ? "light" : "dark";
        document.documentElement.classList.toggle("dark-mode", newTheme === "dark");
        html.setAttribute("data-bs-theme", newTheme);
        // document.body.setAttribute("data-bs-theme", newTheme);
        // tables.forEach(table => table.classList.toggle("dark-mode", newTheme === "dark"));
        // select2Fields.forEach(field => field.classList.toggle("dark-mode", newTheme === "dark"));
        
        localStorage.setItem("theme", newTheme);
        darkModeToggle.innerHTML = newTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";

         // updateSelect2Theme(); // Ensure Select2 adopts the new theme
    });
});
