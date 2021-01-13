function openNav() {

    if (document.getElementById("id_sideBar").offsetWidth == "0") {

        document.getElementById("id_sideBar").style.width = "250px";
        document.getElementById("main_view").style.marginLeft = "250px";
    }
    else{
        document.getElementById("id_sideBar").style.width = "0";
        document.getElementById("main_view").style.marginLeft = "10px";
    }

}

window.onscroll = function() {myFunction();};

var navbar = document.getElementById("id_topnav");
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky");
  } else {
    navbar.classList.remove("sticky");
  }
}

// Get the modal
var modal = document.getElementById("id-functions");
// Get the button that opens the modal
var submitBtn = document.getElementById("id-submit-btn");
// Get the <span> element that closes the modal

var close = document.getElementById("id-functions-close");


// When the user clicks on the button, open the modal
submitBtn.onclick = function() {
    if( document.getElementById("upload_compare").files.length != 0 && document.getElementById("upload_ori").files.length!= 0 ){
  modal.style.display = "block";}
}

// When the user clicks on <span> (x), close the modal
close.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var form = document.getElementById("id-submit-btn");
function handleForm(event) { event.preventDefault(); }
form.addEventListener('submit', handleForm);