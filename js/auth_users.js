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
            // Store token generated to the browser localstorage
               console.log(data["login_message"]["token_generated"]);
               localStorage.setItem('token', data["login_message"]["token_generated"]);
               localStorage.setItem('username', data["login_message"]["username"]);
               window.location.href = "./users_dashboard.html";

           }else {
            // Store token generated to the browser localstorage
            console.log(data["login_message"]["token_generated"]);
            localStorage.setItem('token', data["login_message"]["token_generated"]);
            localStorage.setItem('username', data["login_message"]["username"]);
            window.location.href = "./admin_dashboard.html";
           }

       }else {
        login_error_message.innerHTML = data["login_message"]["message"];
       }

   })
   
}

// function to set user name
function loadFunctionOnLoadingPage() {
    var loggedin_user = document.getElementById('loggedin_user');
    loggedin_user.innerHTML = localStorage.getItem('username');
}

//function to register a user
function RegisterUser(){   
    var firstname = document.getElementById('firstname').value;
    var lastname = document.getElementById('lastname').value;
    var contact = document.getElementById('contact').value;
    var email_address = document.getElementById('email_address').value;
    var password = document.getElementById('password').value;
    var username = document.getElementById('username').value;
    filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(firstname.trim() == ''){
       document.getElementById('error_firstname').style.display = 'block';
       document.getElementById('error_firstname').innerHTML = 'Firstname field is required'; 
       document.getElementById('error_firstname').style.color= '#DC3545';
    }if(lastname.trim() == ''){
        document.getElementById('error_lastname').style.display = 'block';
        document.getElementById('error_lastname').innerHTML = 'Lastname field is required';
        document.getElementById('error_lastname').style.color= '#DC3545'; 
    }if(contact.trim() == '') {
        document.getElementById('error_contact').style.display = 'block';
        document.getElementById('error_contact').innerHTML = 'Phone Contact field is required'; 
        document.getElementById('error_contact').style.color= '#DC3545'; 
    }if(email_address.trim() == '') {
        document.getElementById('error_email_address').style.display = 'block';
        document.getElementById('error_email_address').innerHTML = 'Email field is required';
        document.getElementById('error_email_address').style.color= '#DC3545';  
    }if(password.trim() == '') {
        document.getElementById('error_password').style.display = 'block';
        document.getElementById('error_password').innerHTML = 'Password field is required';
        document.getElementById('error_password').style.color= '#DC3545';  
    }
    if(username.trim() == '') {
        document.getElementById('error_username').style.display = 'block';
        document.getElementById('error_username').innerHTML = 'Username field is required';
        document.getElementById('error_username').style.color= '#DC3545';
        document.getElementById('error_username').style.fontStyle= 'none';    
    }
    
    if (filter.test(email_address)) {
        var new_user  = {
            "first_name":firstname, 
            "last_name":lastname, 
            "email":email_address,
            "phone_contact":contact, 
            "username":username,
            "user_password":password
          }
          alert(JSON.stringify(new_user));
        fetch('http://127.0.0.1:5000/api/v2/auth/signup',
        {
            method:'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(new_user),
            cache:'no-cache'
        })
        .then(function(res){
            return res.json()
        })
        .then(result => {
            
            if(result["message"] === 'You registered successfully, Please Login'){
                var success_signup = document.getElementById('success_signup');
                var success_message = document.getElementById('success_message');
                var message  = 'You registered successfully, Please Login';
                success_signup.style.display='block';
                success_message.innerHTML = message;
                success_message.style.backgroundColor='lightblue';
    
                setTimeout(function(){
                    success_signup.style.display='none';
                }, 3000)
    
            }
            else{
                alert('something went wrong try again')
            }
        
        })
    }
    else
    {
        document.getElementById('error_email_address').style.display = 'block';
        document.getElementById('error_email_address').innerHTML = 'Email entered  is Invalid';
        document.getElementById('error_email_address').style.color= '#DC3545'; 
    }
  
  
    
    }
