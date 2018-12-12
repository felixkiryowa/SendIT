// Function to enable a user to make an order
function Make_A_Parcel_delivery_Order() {
    var order_name = document.getElementById('order_name').value;
    var parcel_weight = document.getElementById('parcel_weight').value;
    var parcel_pickup_address = document.getElementById('parcel_pickup_address').value;
    var parcel_destination_address = document.getElementById('parcel_destination_address').value;
    var receivers_names = document.getElementById('receivers_names').value;
    var receivers_contact = document.getElementById('receivers_contact').value;
   
    var all_fields_required = document.getElementById('all_fields_required');
    var overall_error_message = document.getElementById('overall_error_message');

    // To check empty form fields.
    if (order_name.length == 0 || parcel_weight.length == 0 || parcel_pickup_address.length == 0 || 
        parcel_destination_address.length == 0  || 
        receivers_names.length == 0 || receivers_contact.length == 0)  {
        all_fields_required.style.display='block';
        overall_error_message.innerHTML = "* All fields are required *";
        overall_error_message.style.color= '#DC3545'; 
        return false;
    }

      // Check each input in the order that it appears in the form.
      if (inputAlphabet(order_name, "* Only alphabets required *", "error_order_name")) {
        if(validate_parcel_receivers_names(receivers_names, "* Only alphabets required receivers name*", "error_receivers_names")){
            if (inputAlphabet(parcel_destination_address, "* Only alphabets required *", "error_parcel_destination_address")) {
                if (inputAlphabet(parcel_pickup_address, "* Only alphabets required *", "error_parcel_pickup_address")) {
                    if(textNumeric(parcel_weight, "* Parcel weight should be a number *", "error_parcel_weight")){
                        if(textNumeric(receivers_contact, "* Phone contact consists of only numbers *", "error_receivers_contact")){

                            var parcel_order  = {
                                "order_name":order_name,
                                "parcel_weight":parseInt(parcel_weight), 
                                "parcel_pickup_address":parcel_pickup_address, 
                                "parcel_destination_address":parcel_destination_address, 
                                "receivers_names": receivers_names, 
                                "receivers_contact":receivers_contact
                              }
                              fetch('https://francissendit.herokuapp.com/api/v2/parcels',
                                {
                                    method:'POST',
                                    headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json',
                                        "token":  localStorage.getItem("token")
                                    },
                                    body: JSON.stringify(parcel_order),
                                    cache:'no-cache'
                                })
                                .then(function(res){
                                    return res.json()
                                })
                                .then((result) => {

                                    if(result["message"] === 'Token has expired,please login again'){
                                        alert("Session Has Expired,Please Login Again !!!")
                                        window.location.href="./index.html";
                                    }
                                    
                                    else if(result["message"] === 'Successfully created an order'){
                                        var success_signup = document.getElementById('success_signup');
                                        var success_message = document.getElementById('success_message');
                                        var message  = 'You Have Successfully Created A Parcel Delivery Order';
                                        success_signup.style.display='block';
                                        success_message.innerHTML = message;
                                        success_message.style.backgroundColor='lightblue';

                        
                                        setTimeout(function(){
                                            var deliver_order = document.getElementById("delivery_order");
                                            var order_details = document.getElementById("order_details");
                                            var order_history = document.getElementById("order_history");
                                            var delivery_order_destination = document.getElementById("delivery_order_destination");
                                            document.getElementById('order_name').value = '';
                                            document.getElementById('parcel_weight').value = '';
                                            document.getElementById('parcel_pickup_address').value = '';
                                            document.getElementById('parcel_destination_address').value = '';
                                            document.getElementById('receivers_names').value = '';
                                            document.getElementById('receivers_contact').value = '';
                                            success_signup.style.display='none';
                                            // window.location.href = "./users_dashboard.html";
                                            get_specific_user_orders();
                                            
                                            delivery_order_destination.style.display="none";
                                            deliver_order.style.display = "none";
                                            order_details.style.display ="block";
                                            order_history.style.display="none";
                                            
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

// Function to validate reciever of the parcel names
function validate_parcel_receivers_names(inputtext, alertMsg, element_id){
    var alphaExp = /^\w+(\s\w+)*$/;
    if (inputtext.match(alphaExp)) {
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


// function to fetch specific user orders

    function get_specific_user_orders(){
        fetch('https://francissendit.herokuapp.com/api/v2/users/parcels', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json',
                "token": localStorage.getItem("token")
            },
            cache: 'no-cache'
            
        })
    .then((res) => res.json())
    .then(data => {
        if(data["message"] == 'No Orders Found, You Can Make An Order Now!!!'){
            var no_orders_found = document.getElementById('no_orders_found');
            var no_orders_found_message = document.getElementById('no_orders_found_message');
            var message  = 'No Orders Found, You Can Make An Order Now!!!';
            no_orders_found.style.display='block';
            no_orders_found_message.innerHTML = message;
            // no_orders_found_message.style.backgroundColor='lightblue';
            no_orders_found_message.style.fontStyle='italic';
        }
        else{
            var i = 0;

                var table = '<table class="items_table">'+
                            '<tr>'+
                            '<th>Order Name</th>'+
                            '<th>Order Status</th>'+
                            '<th>Order Details</th>'+
                            '<th>Cancel</th>'+
                           ' </tr>';               
                for(i=0; i < data["Specific_order"].length; i++){
                    var created_at = data["Specific_order"][i]["created_at"];
                    var data_to_string = created_at;
                    var splitting_string = data_to_string.split(",");
                    var string1 = splitting_string[0].toString();
                    var string2 =  splitting_string[1].toString();
                    var ordering_time = data["Specific_order"][i]["ordering_time"];
                    var pickup_address = data["Specific_order"][i]["parcel_pickup_address"];
                    var destination_address =  data["Specific_order"][i]["parcel_destination_address"];
                    
                    table +=  
                    '<tr><td>'+data["Specific_order"][i]["order_name"]
                    +'</td><td>'+data["Specific_order"][i]["order_status"]
                    +'</td><td><button class="order_details_button" onclick="MakeOrder1('+data["Specific_order"][i]["parcel_order_id"]+')">Order Details</button>'
                    +'</td><td><button class="order_cancel_button" onclick="CancelOrder('+data["Specific_order"][i]["parcel_order_id"]+')">Cancel Order</button>'
                    +'</td>';
                }
                document.getElementById("user_orders_table").innerHTML = table+"</table>";
            
        }
        
    })

    }

    get_specific_user_orders();



    function Update_parcel_order_destination() {
        var order_number_to_update = document.getElementById("order_number_to_update").value;
        var new_order_destination = document.getElementById("new_order_destination").value;
        if(new_order_destination == ''){
            alert("New Destination field  is Required");
        }else {
        var parcel_id = parseInt(order_number_to_update);

        var parcel_order_destination  = {
            "parcel_destination_address":new_order_destination
        }
        fetch('https://francissendit.herokuapp.com/api/v2/parcels/'+parcel_id+'/destination',
            {
                method:'PUT',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    "token":  localStorage.getItem("token")
                },
                body: JSON.stringify(parcel_order_destination),
                cache:'no-cache'
            })
            .then((res) => res.json())
            .then(data => {
                var change_destination = document.getElementById('change_destination');
                var destination_error_message = document.getElementById('destination_error_message');
                 if(data["message"] == 'The order is delivered already so its destination cannot be updated'){
                    change_destination.style.display='block';
                    destination_error_message.innerHTML = "The order is delivered already so its destination cannot be updated";
                    destination_error_message.style.color= '#DC3545'; 

                 }else if(data["message"] == 'The order is cancelled already so its destination cannot be updated'){
                    change_destination.style.display='block';
                    destination_error_message.innerHTML = "The order is cancelled already so its destination cannot be updated";
                    destination_error_message.style.color= '#DC3545'; 
                 }
                 else{

                    var success_destination_update = document.getElementById('success_destination_update');
                    var success_message_destination_update = document.getElementById('success_message_destination_update');
                    // var message  = 'You Have Successfully Updated The Parcel Delivery Order Destination';
                    success_destination_update.style.display='block';
                    success_message_destination_update.innerHTML = data["message"];
                    success_message_destination_update.style.backgroundColor='lightblue';

                    setTimeout(function(){
                        var deliver_order = document.getElementById("delivery_order");
                        var order_details = document.getElementById("order_details");
                        var order_history = document.getElementById("order_history");
                        var delivery_order_destination = document.getElementById("delivery_order_destination");
                        document.getElementById('new_order_destination').value = '';
                        
                        success_message_destination_update.style.display='none';
                        // window.location.href = "./users_dashboard.html";
                        get_specific_user_orders();
                        
                        delivery_order_destination.style.display="none";
                        deliver_order.style.display = "none";
                        order_details.style.display ="block";
                        order_history.style.display="none";
                        
                    }, 3000)
                 }
            })
        }
   
    }

//function to cancel an order
function CancelOrder(parcel_id){
    var x = confirm("Are you  sure you want to cancel an order?");
    if(x) {
        var order_status  = {
            "order_status":"cancelled"
        }
        fetch('https://francissendit.herokuapp.com/api/v2/parcels/'+parcel_id+'/cancel',
        {
            method:'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "token":  localStorage.getItem("token")
            },
            body: JSON.stringify(order_status),
            cache:'no-cache'
        })
        .then((res) => res.json())
        .then(data => {
           if(data["message"] == 'The order is delivered already'){
               alert("The order is delivered already");
           }else if(data["message"] == 'The order is cancelled already'){
               alert("The order is cancelled already");
           }else{
               alert("You Have Successfully Cancelled The Parcel Delivery Order");
            //    window.location.href="./users_dashboard.html";
            var deliver_order = document.getElementById("delivery_order");
            var order_details = document.getElementById("order_details");
            var order_history = document.getElementById("order_history");
            var delivery_order_destination = document.getElementById("delivery_order_destination");
            // window.location.href = "./users_dashboard.html";
            get_specific_user_orders();
            
            delivery_order_destination.style.display="none";
            deliver_order.style.display = "none";
            order_details.style.display ="block";
            order_history.style.display="none";
           }
        })
    }else {
        
    }
   
}

// Function to fetch all orders
fetch('https://francissendit.herokuapp.com/api/v2/parcels', {
    method: 'GET',
    headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        "token": localStorage.getItem("token")
    },
    cache: 'no-cache'
    
})
    .then((res) => res.json())
    .then(data => {
        if(data["message"] == 'No Order Entries Found !!'){
            var no_orders_found = document.getElementById('no_orders_found');
            var no_orders_found_message = document.getElementById('no_orders_found_message');
            var message  = 'No Order Entries Found !!';
            no_orders_found.style.display='block';
            no_orders_found_message.innerHTML = message;
            // no_orders_found_message.style.backgroundColor='lightblue';
            no_orders_found_message.style.fontStyle='italic';
        }
        else{
            var i = 0;

                var table = '<table class="items_table">'+
                            '<tr>'+
                            '<th>Order ID</th>'+
                            '<th>Order Name</th>'+
                            '<th>Weight(kg)</th>'+
                            '<th>Order Price(shs)</th>'+
                            '<th>Order Date / Time</th>'+
                            '<th>Order Status</th>'+
                            '<th>Order Location</th>'+
                            '<th>Pickup Address Details</th>'+
                            '<th>Destination Address Details</th>'+
                            '<th>Update Order Status</th>'+
                            '<th>Update Order Location</th>'+
                            ' </tr>';               
                for(i=0; i < data["All_orders"].length; i++){
                    table +=  
                    '<tr><td>'+data["All_orders"][i]["parcel_order_id"]
                    +'</td><td>'+data["All_orders"][i]["order_name"]
                    +'</td><td>'+data["All_orders"][i]["parcel_weight"]
                    +'</td><td>'+data["All_orders"][i]["price"]
                    +'</td><td>'+data["All_orders"][i]["created_at"]
                    +'</td><td>'+data["All_orders"][i]["order_status"]
                    +'</td><td>'+data["All_orders"][i]["order_current_location"]
                    +'</td><td><button class="order_admin_button" onclick="SendersDetails('+data["All_orders"][i]["parcel_order_id"]+')">View more</button>'
                    +'</td><td><button class="order_admin_button" onclick="ReceiversDetails('+data["All_orders"][i]["parcel_order_id"]+')">View more</button>'
                    +'</td><td><button class="order_admin_button" onclick="updateOrderStatus('+data["All_orders"][i]["parcel_order_id"]+')">Update status</button>'
                    +'</td><td><button class="order_admin_button" onclick="UpdateOrderLocation('+data["All_orders"][i]["parcel_order_id"]+')">Update location</button>'
                    +'</td>';
                }
                document.getElementById("all_customer_orders").innerHTML = table+"</table>";
            
        }
        
    })

    function logout_user(event) {
        event.preventDefault();
        var x = confirm("Are you  sure you want to log out?");
        if(x){
          var token = localStorage.getItem('token');
          var used_token =  {
            "user_token": token
          }

          fetch('https://francissendit.herokuapp.com/api/v2/auth/blacklisttoken',
          {
              method:'POST',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(used_token),
              cache:'no-cache'
          })
          .then(function(res){
              return res.json()
          })
          .then((result) => {

              if(result["message"] === 'success'){
                localStorage.removeItem('username');
                localStorage.removeItem('token');

                window.location.href = "./index.html";

              }
               
          })

          
        }else{
        //   alert("cancel");
        }
    }
