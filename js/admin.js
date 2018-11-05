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

function SendersDetails() {
    sendersModal.style.display = "block";
}

function ReceiversDetails() {
    receiversModal.style.display = "block";
}

function updateOrderStatus() {
    updateOrderStatusModal.style.display ="block";
}

function UpdateOrderLocation() {
    updateLocationStatusModal.style.display = "block";
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
