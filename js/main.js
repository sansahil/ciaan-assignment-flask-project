// DOM Content Loaded Event Listener
document.addEventListener("DOMContentLoaded", () => {
  // Handle Flash Messages Auto-Close
  const flashMessages = document.querySelectorAll(".flash-message");
  flashMessages.forEach((message) => {
    setTimeout(() => {
      message.style.opacity = "0"; // Fade out
      setTimeout(() => message.remove(), 500); // Remove after fade
    }, 3000); // Auto-close after 3 seconds
  });

  // Example: Toggle Navigation for Small Screens
  const toggleNav = document.querySelector("#toggle-nav");
  const navMenu = document.querySelector("nav");
  if (toggleNav && navMenu) {
    toggleNav.addEventListener("click", () => {
      navMenu.classList.toggle("hidden");
    });
  }

  // Example: Form Validation (Reset Password Form)
  const resetForm = document.querySelector("#reset-password-form");
  if (resetForm) {
    resetForm.addEventListener("submit", (e) => {
      const emailInput = resetForm.querySelector("input[type='email']");
      if (!emailInput.value) {
        e.preventDefault();
        alert("Please enter a valid email address.");
      }
    });
  }
});
