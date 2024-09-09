alert("hello world!");

// Example: Making a get request to get parcel endpoint
$.ajax({
    url: 'http://127.0.0.1:5000/parcels',
    type: 'GET',
    contentType: 'application/json',
    success: function(response) {
        alert('Parcel added successfully!');
    },
    error: function(err) {
        console.log('Error:', err);
        alert('Failed to add parcel');
    }
});
