// This is authentication file which contains login and logout details
console.log("sa");

$("#loginForm").on("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission

  var formData = {
    email: $("#email").val(),
    password: $("#password").val(),
  };

  $.ajax({
    url: "http://127.0.0.1:5000/login",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(formData),
    success: function (response) {
      if (response.success) {
        // Redirect to make delivery page after successful login
        window.location.href = "http://127.0.0.1:5000/delivery";
      } else {
        alert("Invalid credentials");
      }
    },
    error: function (err) {
      alert("Login failed");
      console.log("Error:", err);
    },
  });
});
