const userData = {
  name: 'John Doe',
  email: 'john.doe@example.com'
};

fetch('http://127.0.0.1:5000/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(userData)
})
.then(response => response.json())
.then(data => {
  console.log('User created:', data);
})
.catch(error => console.error('Error:', error));

// Fetch users from the backend
fetch('http://127.0.0.1:5000/users')
  .then(response => response.json())
  .then(data => {
    console.log(data);  // Data from the backend
    // Update your HTML with user data
  })
  .catch(error => console.error('Error:', error));
