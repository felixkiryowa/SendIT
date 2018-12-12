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

   if(username.length == 0 || password.length == 0) {
    login_error_message.innerHTML = 'All Fields Are Required !!';

   }else {
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
               localStorage.setItem('token', data["login_message"]["token_generated"]);
               localStorage.setItem('username', data["login_message"]["username"]);
               window.location.href = "./users_dashboard.html";

           }else {
            // Store token generated to the browser localstorage
            localStorage.setItem('token', data["login_message"]["token_generated"]);
            localStorage.setItem('username', data["login_message"]["username"]);
            window.location.href = "./admin_dashboard.html";
            
           }

       }
       else  {
        login_error_message.innerHTML = data["login_message"]["message"];
       }

   })
  }
   
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
    var confrim_password = document.getElementById("confrim_password").value;
    
    var all_fields_required = document.getElementById('all_fields_required');
    var overall_error_message = document.getElementById('overall_error_message');

    // To check empty form fields.
    if (firstname.length == 0 || lastname.length == 0 || contact.length == 0 || email_address.length == 0  || 
        password == 0 || username == 0)  {
        all_fields_required.style.display='block';
        overall_error_message.innerHTML = "* All fields are required *";
        overall_error_message.style.color= '#DC3545'; 
        return false;
    }
    // Check each input in the order that it appears in the form.
    if (inputAlphabet(firstname, "* Only alphabets required *", "error_firstname")) {
        if(inputAlphabet(lastname, "* Only alphabets required *", "error_lastname")){
                if (emailValidation(email_address, "* Ivalid email address *")) {
                        if(textNumeric(contact, "* Phone contact consists of only numbers *", "error_contact")){
                            if (textAlphanumeric(username, "* Username consists of both numbers and characters *", "error_username")) {
                                 if(check_password_confrimation(password,confrim_password,"Passwords Do Not Match",
                                 "error_confrim_password")){
                                var new_user  = {
                                    "first_name":firstname, 
                                    "last_name":lastname, 
                                    "email":email_address,
                                    "phone_contact":contact, 
                                    "username":username,
                                    "user_password":password
                                  }
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
                                    .then((result) => {
                                        
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
                                return true;
                                }
                            }
                        }

                }
            
        }
       
    }
    return false;
    }

    // Function that checks whether input text is numeric or not.
    function textNumeric(inputtext, alertMsg, element_id) {
        var numericExpression = /^[0-9]+$/;
        if (inputtext.match(numericExpression)) {
            return true;
        } else {
            document.getElementById(element_id).style.display = 'block';
            document.getElementById(element_id).innerHTML = alertMsg;
            document.getElementById(element_id).style.color= '#DC3545'; 
            
            return false;
        }
    }
    // Function to check confirm password
    function check_password_confrimation(inputtext1,inputtext2, alertMsg, element_id) {
        if (inputtext1 === inputtext2) {
            return true;
        } else {
            document.getElementById(element_id).style.display = 'block';
            document.getElementById(element_id).innerHTML = alertMsg;
            document.getElementById(element_id).style.color= '#DC3545';
        return false;
        }
    }
    // Function that checks whether input text is an alphabetic character or not.
    function inputAlphabet(inputtext, alertMsg, element_id) {
        var alphaExp = /^[a-zA-Z]+$/;
        if (inputtext.match(alphaExp)) {
            return true;
        } else {
            document.getElementById(element_id).style.display = 'block';
            document.getElementById(element_id).innerHTML = alertMsg;
            document.getElementById(element_id).style.color= '#DC3545';
        return false;
        }
    }
    // Function that checks whether input text includes alphabetic and numeric characters.
    function textAlphanumeric(inputtext, alertMsg, element_id) {
        var alphaExp = /^[0-9a-zA-Z]+$/;
        if (inputtext.match(alphaExp)) {
            return true;
        } else {
            document.getElementById(element_id).style.display = 'block';
            document.getElementById(element_id).innerHTML = alertMsg;
            document.getElementById(element_id).style.color= '#DC3545'; 
            return false;
        }
    }
    // Function that checks whether the input characters are restricted according to defined by user.
    function lengthDefine(inputtext, min, max, element_id) {
        var uInput = inputtext;
        if (uInput.length >= min && uInput.length <= max) {
            return true;
        } else {
            document.getElementById(element_id).style.display = 'block';
            document.getElementById(element_id).innerHTML = "* Please enter between " + min + " and " + max + " characters *";
            document.getElementById(element_id).style.color= '#DC3545';
            return false;
        }
    }
    // Function to check password length
    function passwordLength(inputtext, min, max) {
        var uInput = inputtext;
        if (uInput.length >= min && uInput.length <= max) {
            return true;
        } else {
            document.getElementById('error_password').style.display = 'block';
            document.getElementById('error_password').innerHTML = "* Please enter between " + min + " and " + max + " characters *";
            document.getElementById('error_password').style.color= '#DC3545'; 
            return false;
        }
    }
    // Function that checks whether an user entered valid email address or not 
    function emailValidation(inputtext, alertMsg) {
        var emailExp = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if (inputtext.match(emailExp)) {
            return true;
        } else {
            document.getElementById('error_email_address').style.display = 'block';
            document.getElementById('error_email_address').innerHTML = alertMsg;
            document.getElementById('error_email_address').style.color= '#DC3545';
            return false;
        }
    }
    