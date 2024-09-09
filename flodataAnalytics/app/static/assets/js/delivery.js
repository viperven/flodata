document.addEventListener("DOMContentLoaded", function () {
  const senderIdField = document.getElementById("senderId");
  const fileInput = document.getElementById("file");
  const deliveryForm = document.getElementById("deliveryForm");

  // Fetch user details and automatically set sender ID
  fetch("/get-user-details")
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        senderIdField.value = data.user_id; // Set the sender ID from the server
      } else {
        console.error("Failed to get user details");
      }
    });

  deliveryForm.addEventListener("submit", function (event) {
    debugger;
    event.preventDefault();

    const file = fileInput.files[0];
    const formData = new FormData();

    // Check if a file is selected (for bulk upload)
    if (file) {
      formData.append("file", file);
    } else {
      // Handle single parcel form submission
      const receiverName = document.getElementById("receiverName").value;
      const receiverAddress = document.getElementById("receiverAddress").value;
      const weight = document.getElementById("weight").value;
      const status = "pending";

      // Ensure all fields are filled
      if (!receiverName || !receiverAddress || !weight || !status) {
        alert("Please fill all the fields.");
        return;
      }

      // Append single parcel data to formData
      formData.append("sender_id", senderIdField.value); // Set sender ID
      formData.append("receiver_name", receiverName);
      formData.append("receiver_address", receiverAddress);
      formData.append("weight", weight);
      formData.append("status", status);
    }

    // Submit the form via Fetch API
    fetch("/make_delivery", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          if (data.bulk_task_id) {
            document.getElementById(
              "orderNumber"
            ).textContent = `Bulk Task ID: ${data.bulk_task_id}`;
            alert(`Bulk Task ID: ${data.bulk_task_id}`);
          } else {
            alert(
              `Parcel added successfully ${data?.tracking_number} For Single Parcel`
            );
          }
        } else {
          console.error("Error submitting delivery:", data.message);
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});
