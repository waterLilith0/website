// Utility to dynamically switch between light.css and dark.css
function setThemeCss(theme) {
  // Remove any existing theme stylesheet
  let lightLink = document.getElementById('light-css');
  let darkLink = document.getElementById('dark-css');

  if (lightLink) lightLink.remove();
  if (darkLink) darkLink.remove();

  // Add the correct stylesheet
  const head = document.head;
  if (theme === "dark") {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'css/dark.css';
    link.id = 'dark-css';
    head.appendChild(link);
  } else {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'css/light.css';
    link.id = 'light-css';
    head.appendChild(link);
  }
}

const darkModeToggle = document.querySelector("#darkModeToggle");

function applyTheme(theme) {
  setThemeCss(theme); // This swaps the stylesheet <link>

  // NEW: Add logic to update body class
  if (theme === "dark") {
    document.body.classList.add("dark-mode-v1");
    document.body.classList.remove("light-mode");
    // Ensure the toggle is correctly checked
    if (darkModeToggle) darkModeToggle.checked = true;
  } else {
    document.body.classList.add("light-mode");
    document.body.classList.remove("dark-mode-v1");
    // Ensure the toggle is correctly UNchecked
    if (darkModeToggle) darkModeToggle.checked = false;
  }
}

// On script load
document.addEventListener("DOMContentLoaded", () => {
  // Initialize Materialize components like Sidenav
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems); // Moved Sidenav init here to ensure body is set first

  const savedTheme = localStorage.getItem("theme");
  // Default to light theme if nothing is saved or if saved value is invalid
  if (savedTheme === "dark") {
    applyTheme("dark");
  } else {
    applyTheme("light"); // Default to light
  }
});

if (darkModeToggle) {
  darkModeToggle.addEventListener("change", () => {
    if (darkModeToggle.checked) {
      localStorage.setItem("theme", "dark");
      applyTheme("dark");
    } else {
      localStorage.setItem("theme", "light");
      applyTheme("light");
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems);
});