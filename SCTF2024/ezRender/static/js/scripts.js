function show_hide_password(target){
    var input = document.getElementById('password-input');
    if (input.getAttribute('type') == 'password') {
     target.classList.add('view');
     input.setAttribute('type', 'text');
    } else {
     target.classList.remove('view');
     input.setAttribute('type', 'password');
    }
    return false;
   }
   
   document.addEventListener('DOMContentLoaded', function() {
       document.querySelector('form').addEventListener('submit', function(event) {
           event.preventDefault();
           const path = document.querySelector('input[name="submit"]').value;
           var loc;
           const formData = {
               username: document.querySelector('input[name="username"]').value,
               password: document.querySelector('input[name="password"]').value
           };
           if (path === "login") {
               loc = "admin";
           }
           if (path === "register") {
               loc = "login";
           }
   
           fetch(`/${path}`, {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify(formData),
               credentials: 'include'  // Ensure cookies are included in the request and response
           })
           .then(response => {
               if (response.ok) {
                   window.location.href = `/${loc}`;
               } else {
                   console.error('Failed to authenticate');
               }
           })
           .catch(error => console.error('Error:', error));
       });
   });