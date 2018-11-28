// var url = 'https://francissendit.herokuapp.com/api/v2/parcels/1';

// fetch(url).then(response => response.json).then(data => console.log(data))

// function to  handle user login into the application
function authenticateusers() {
    var url = 'http://127.0.0.1:5000/api/v2/auth/login';

    var username = document.getElementById('user_name').value;
    var password = document.getElementById('user_password').value;
    var login_error_message = document.getElementById('login_error_message');
    var  new_user = {
	 
        "username":username,
        "password":password
   }
   fetch(url, {
       method:'POST',
       headers: {
           'Accept':'application/json',
           'Content-Type':'application/json'
       },
       cache:'no-cache',
       body:JSON.stringify(new_user)
   })
   .then(response => response.json())
   .then(data => 
    {
       if(data["login_message"]["message"] == 'successfully loggedin') {
           if(data["login_message"]["user_role"] == 'user') {
               window.location.href = "./users_dashboard.html";

           }else {
            window.location.href = "./admin_dashboard.html";
           }

       }else {
        login_error_message.innerHTML = data["login_message"]["message"];
       }

   })
   
}
