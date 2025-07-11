  <script>
  const storedTheme = localStorage.getItem("theme");
  if (storedTheme === "dark") {
    document.documentElement.classList.add("dark-mode");
    document.documentElement.setAttribute("data-bs-theme", "dark");
  } else {
    // Handles 'light' or if theme is not set (null), default to light
    document.documentElement.classList.remove("dark-mode");
    document.documentElement.setAttribute("data-bs-theme", "light");
  }
  </script>