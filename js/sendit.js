window.onscroll = function() {myFunction()};
 var header = document.getElementById("site_navbar");
var sticky = header.offsetTop;
 function myFunction() {
  if (window.pageYOffset > sticky) {  
    header.classList.add("sticky");
    document.getElementById("site_navbar").style.backgroundColor = "black";
    document.getElementById("site_navbar").style.height="80px";
  } else {
    header.classList.remove("sticky");
    document.getElementById("site_navbar").style.backgroundColor = "";
  }
}

// make order function
function MakeOrder(){
    
    var make_order = document.getElementById("make_order");
    var content_holder = document.getElementById("content_holder");
    var order_history = document.getElementById("order_history");
    order_history.style.display = "none";
    content_holder.style.display ="none";
    make_order.style.display = "block";
    
}
//returning back to home
function BackHome(){
    var make_order = document.getElementById("make_order");
    var content_holder = document.getElementById("content_holder");
    var order_history = document.getElementById("order_history");
    order_history.style.display ="none";
    // make_order.style.display = "none"; 
    content_holder.style.display ="block";
     
}
//view ordering history
function ViewHistory(){
    var order_history = document.getElementById("order_history");
    var make_order = document.getElementById("make_order");
    var content_holder = document.getElementById("content_holder");
    // make_order.style.display = "none"; 
    content_holder.style.display ="none";
    order_history.style.display = "block"
}
//manage fast-food-items
function ManageItems(){
    var EditItem = document.getElementById("EditItem");
    var addItem = document.getElementById("addItem");
    var food_items = document.getElementById("food_items");
    var customer_orders = document.getElementById("customer_orders");
    addItem.style.display ="none";
    customer_orders.style.display="none";
    EditItem.style.display="none";
    food_items.style.display="block";

}
//manage orders
function ManageOrders(){
    var EditItem = document.getElementById("EditItem");
    var addItem = document.getElementById("addItem");
    var food_items = document.getElementById("food_items");
    var customer_orders = document.getElementById("customer_orders");
    addItem.style.display ="none";
    food_items.style.display="none";
    EditItem.style.display="none";
    customer_orders.style.display="block";
}
//function to delete fast-food-fast items
function CancelOrder(){
    alert("Order Cancelled !! ");
}

//authenticating admins
function authenticateadmins(){
    var user_email = document.getElementById("user_email").value;
    var user_password = document.getElementById("user_password").value;
    if(user_email === "admin@gmail.com" && user_password === "admin123"){
        //redirecting to user dashboard
         window.location.href="admin_dashboard.html";
        //console.log("Fine");
    }else{
         //window.location.href="user_dashboard.html";
         alert("Invalid Email or Password!");
    }
}
//authenticating users
function authenticateusers(){
    var user_email = document.getElementById("user_email").value;
    var user_password = document.getElementById("user_password").value;
    
    if(user_email === "user@gmail.com" && user_password === "user123"){
        //redirecting to user dashboard
         window.location.href="user_dashboard.html";
        //console.log("Fine");
    }else{
         //window.location.href="user_dashboard.html";
         alert("Invalid Email or Password!");
    }
}

//defining what happens when a user clicks the signup button
document.getElementById("register").addEventListener("click",function(){
    var cards = document.getElementById('services_cards');
    var all_sections = document.querySelectorAll("section");
    var login_user_form = document.getElementById('site_login_form');
    var site_signup_form = document.getElementById('site_signup_form');
    document.body.style.backgroundImage="url(images/image3.jpg)";

    var i;
    for (i = 0; i < all_sections.length; i++) {
        all_sections[i].style.display = "none";
    }
    
    login_user_form.style.display = "none";
    cards.style.display = "none";
    site_signup_form.style.display = "block";
     
});

//Adding action when user clicks on the login link in navbar
document.getElementById("enter_account").addEventListener("click",function(){
    var all_sections = document.querySelectorAll("section");
    var cards = document.getElementById('services_cards');
    var login_user_form = document.getElementById('site_login_form');
    var site_signup_form = document.getElementById('site_signup_form');
    var i;
    for (i = 0; i < all_sections.length; i++) {
        all_sections[i].style.display = "none";
    }
    cards.style.display = "none";
    site_signup_form.style.display="none";
    login_user_form.style.display = "block";

     
});

//Adding action when user clicks on the home link in navbar
document.getElementById("site_home").addEventListener("click",function(){
    var get_sections = document.getElementById("site_section");
    var cards = document.getElementById('services_cards');
    var login_user_form = document.getElementById('site_login_form');
    var site_signup_form = document.getElementById('site_signup_form');
    get_sections.style.display = "block"
    cards.style.display = "none";
    site_signup_form.style.display="none";
    login_user_form.style.display = "none";

     
});


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function DropDown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
} 

// Get the modal
var modal = document.getElementById('myModal');
var GoogleModal = document.getElementById("GoogleModal");


// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var close2  = document.getElementsByClassName("close2")[0];

function MakeOrder1(){
    modal.style.display = "block";
}

function GoogleMap() {
  GoogleModal.style.display ="block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}
close2.onclick = function() {
    GoogleModal.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }else if(event.target == GoogleModal) {
        GoogleModal.style.display = "none";
    }
}

// function to allow user to change destination
function changeDestination() {
    var destination = document.getElementById("destination");
    var place = document.getElementById("place");
    var newdestination = document.getElementById("newdestination");
    var save_button_destination = document.getElementById("save_button_destination");
    var cancel_buttton_destination =  document.getElementById("cancel_buttton_destination");
    destination.style.display = "none";
    place.style.display="none";
    newdestination.style.display = "block";
    save_button_destination.style.display = "block";
    cancel_buttton_destination.style.display="block";
    
}


/* When the user clicks on the button,toggle between hiding and showing the dropdown content */
function viewNotifications() {
    var view_notifications = document.getElementById("view_notifications");
    view_notifications.style.display = "block";
    document.getElementById("notifications_drop_down").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
if (!event.target.matches('.imagedropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
    }
    }
}
}

// function to execute when a user clicks on order details option on navbar
function OrderDetails(){
    var deliver_order = document.getElementById("delivery_order");
    var order_details = document.getElementById("order_details");
    var order_history = document.getElementById("order_history");
    deliver_order.style.display = "none";
    order_history.style.display="none";
    order_details.style.display ="block";
}
// function to execute when a user clicks on order history menu
function OrderHistory() {
    var deliver_order = document.getElementById("delivery_order");
    var order_details = document.getElementById("order_details");
    var order_history = document.getElementById("order_history");

    deliver_order.style.display = "none";
    order_details.style.display ="none";
    order_history.style.display="block";
}

// function to execute when a user clicks on  home menu link
function DashboardHome() {
    var deliver_order = document.getElementById("delivery_order");
    var order_details = document.getElementById("order_details");
    var order_history = document.getElementById("order_history");

    deliver_order.style.display = "block";
    order_details.style.display ="none";
    order_history.style.display="none";
}










