// Get the modal
var sendersModal = document.getElementById("sendersModal");
var receiversModal = document.getElementById("receiversModal");
var updateOrderStatusModal = document.getElementById("updateOrderStatusModal");
var updateLocationStatusModal = document.getElementById("updateLocationStatusModal");


// Get the <span> element that closes the modal
var close1 = document.getElementsByClassName("close1")[0];
var close2 = document.getElementsByClassName("close2")[0];
var close3 = document.getElementsByClassName("close3")[0];
var close4 = document.getElementsByClassName("close4")[0];


function updateOrderStatus(parcel_id) {
    updateOrderStatusModal.style.display ="block";
    document.getElementById("parcel_order_id").value = parcel_id;
}

function UpdateOrderLocation(parcel_id) {
    updateLocationStatusModal.style.display = "block";
    document.getElementById('specific_parcel_order_id').value = parcel_id;
}

// When the user clicks on <span> (x), close the modal
close1.onclick = function() {
    sendersModal.style.display = "none";
}

close2.onclick = function() {
    receiversModal.style.display = "none";
}
close3.onclick = function() {
    updateOrderStatusModal.style.display = "none";
}
close4.onclick = function() {
    updateLocationStatusModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == sendersModal) {
        sendersModal.style.display = "none";
    }else if(event.target == receiversModal) {
        receiversModal.style.display = "none";
    }
    else if(event.target == updateOrderStatusModal) {
        updateOrderStatusModal.style.display = "none";
    }
    else if(event.target == updateLocationStatusModal) {
        updateLocationStatusModal.style.display = "none";
    }

}


function SendersDetails(parcel_id){
    fetch('http://127.0.0.1:5000/api/v2/parcels/'+parcel_id,
        {
            method:'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "token":  localStorage.getItem("token")
            },
            cache:'no-cache'
        })
        .then((res) => res.json())
        .then(data => {
            
            sendersModal.style.display = "block";
            var order_pickup_location = document.getElementById("order_pickup_location");
            var senders_email = document.getElementById("senders_email");
            var senders_contact = document.getElementById("senders_contact");
            var senders_names = document.getElementById("senders_names");
            
            order_pickup_location.innerHTML = data["Specific_order"][0]["parcel_pickup_address"];
            senders_email.innerHTML = data["Specific_order"][0]["senders_email"];
            senders_contact.innerHTML = data["Specific_order"][0]["senders_phonecontact"];
            senders_names.innerHTML =  data["Specific_order"][0]["senders_firstname"] + " " + data["Specific_order"][0]["senders_lastname"]
        
        })

}

function ReceiversDetails(parcel_id) {
    fetch('http://127.0.0.1:5000/api/v2/parcels/'+parcel_id,
        {
            method:'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "token":  localStorage.getItem("token")
            },
            cache:'no-cache'
        })
        .then((res) => res.json())
        .then(data => {
            
            receiversModal.style.display = "block";
            var order_destination_location = document.getElementById("order_destination_location");
            var receivers_contact = document.getElementById("receivers_contact");
            var receivers_names = document.getElementById("receivers_names");
            
            order_destination_location.innerHTML = data["Specific_order"][0]["parcel_destination_address"];
            receivers_contact.innerHTML = data["Specific_order"][0]["receivers_contact"];
            receivers_names.innerHTML =  data["Specific_order"][0]["receivers_names"];
        
        })
}

function updateOrderStatusAdmin(event){
    event.preventDefault();
    var get_status = document.getElementById("get_status").value;
    var parcel_order_id = document.getElementById("parcel_order_id").value;
    alert(parcel_order_id);
    var new_order_status  = {
        "order_status":get_status
    }
    fetch('http://127.0.0.1:5000/api/v2/parcels/'+parseInt(parcel_order_id)+'/status',
        {
            method:'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "token":  localStorage.getItem("token")
            },
            body: JSON.stringify(new_order_status),
            cache:'no-cache'
        })
        .then((res) => res.json())
        .then(data => {
            var change_order_status = document.getElementById('change_order_status');
            var change_order_error_message = document.getElementById('change_order_error_message');
             if(data["message"] == 'The parcel order  is already cancelled'){
                change_order_status.style.display='block';
                change_order_error_message.innerHTML = "The parcel order  is already cancelled";
                change_order_error_message.style.color= '#DC3545'; 
                setTimeout(function(){
                    window.location.href = "./admin_dashboard.html";
                }, 5000) 

             }else if(data["message"] == 'The parcel order  is already delivered'){
                change_order_status.style.display='block';
                change_order_error_message.innerHTML = "The parcel order  is already delivered";
                change_order_error_message.style.color= '#DC3545';
                setTimeout(function(){
                    window.location.href = "./admin_dashboard.html";
                }, 5000) 
             }
             else{

                var success_order_status_update = document.getElementById('success_order_status_update');
                var success_message_order_status = document.getElementById('success_message_order_status');
                
                success_order_status_update.style.display='block';
                success_message_order_status.innerHTML = 'Order Status Has Been successfully Updated';
                success_message_order_status.style.backgroundColor='lightblue';

                setTimeout(function(){
                    window.location.href = "./admin_dashboard.html";
                }, 5000) 
             }
        })

}


function   updateOrderLocationAdmin(event) {
    event.preventDefault();
    var order_location = document.getElementById("order_location").value;
    alert(order_location);
    var specific_parcel_order_id= document.getElementById("specific_parcel_order_id").value;
    
    var new_order_location  = {
        "parcel_location":order_location
    }
    fetch('http://127.0.0.1:5000/api/v2/parcels/'+parseInt(specific_parcel_order_id)+'/presentlocation',
        {
            method:'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "token":  localStorage.getItem("token")
            },
            body: JSON.stringify(new_order_location),
            cache:'no-cache'
        })
        .then((res) => res.json())
        .then(data => {
            var change_order_location = document.getElementById('change_order_location');
            var change_order_location_error_message = document.getElementById('change_order_location_error_message');
             if(data["message"] == 'The order is cancelled already'){
                change_order_location.style.display='block';
                change_order_location_error_message.innerHTML = "The parcel order  is already cancelled";
                change_order_location_error_message.style.color= '#DC3545'; 
                setTimeout(function(){
                    window.location.href = "./admin_dashboard.html";
                }, 5000) 

             }else if(data["message"] == 'The order is delivered already'){
                change_order_location.style.display='block';
                change_order_location_error_message.innerHTML = "The parcel order  is already delivered";
                change_order_location_error_message.style.color= '#DC3545';
                setTimeout(function(){
                    window.location.href = "./admin_dashboard.html";
                }, 5000) 
             }
             else{

                var success_order_location_update = document.getElementById('success_order_location_update');
                var success_message_order_location = document.getElementById('success_message_order_location');
                
                success_order_location_update.style.display='block';
                success_message_order_location.innerHTML = 'Order Status Has Been successfully Updated';
                success_message_order_location.style.backgroundColor='lightblue';

                setTimeout(function(){
                    window.location.href = "./admin_dashboard.html";
                }, 5000) 
             }
        })

}
