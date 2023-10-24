let subMenu = document.getElementById("profile-subMenu")

function toggleMenu() {
    subMenu.classList.toggle("open-menu")
}

// document.getElementById('approvalrequest').addEventListener('click', function() {
//     // Send a POST request to the create_record view
//     fetch('/create-approval/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf_token  // Make sure to include the CSRF token
//         },
//         body: JSON.stringify({})
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data.message);
//         alert('Approval request sent');
//     })
//     .catch(error => console.error('Error:', error));
// });