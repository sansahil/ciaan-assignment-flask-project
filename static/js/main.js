document.addEventListener("DOMContentLoaded", function () {
  // Select buttons based on their classes
  const signupBtn = document.querySelector(".bg-[#F4511E]"); // Replace with correct class
  const signinBtn = document.querySelector(".border-[#F4511E]"); // Replace with correct class

  // Redirect to the sign-up page
  if (signupBtn) {
      signupBtn.addEventListener("click", function () {
          window.location.href = "/signup"; // Replace with your actual sign-up URL
      });
  }

  // Redirect to the sign-in page
  if (signinBtn) {
      signinBtn.addEventListener("click", function () {
          window.location.href = "/signin"; // Replace with your actual sign-in URL
      });
  }

  // Optional: Header Sign-up Button Logic
  const headerSignupBtn = document.querySelector("header button"); // Update selector if necessary
  if (headerSignupBtn) {
      headerSignupBtn.addEventListener("click", function () {
          window.location.href = "/signup"; // Redirect to the sign-up page
      });
  }
});
