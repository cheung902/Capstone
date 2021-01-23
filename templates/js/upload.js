function openNav() {

    if (document.getElementById("id_sideBar").offsetWidth == "0") {

        document.getElementById("id_sideBar").style.width = "250px";
        document.getElementById("main_view").style.marginLeft = "250px";
        document.getElementById("id_sideBar").style.borderRight = "1px solid #f2f2f2";
    }
    else{
        document.getElementById("id_sideBar").style.width = "0";
        document.getElementById("main_view").style.marginLeft = "10px";
        document.getElementById("id_sideBar").style.borderRight = "none";
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

var comp_before_upload = document.getElementById("comp_before_upload")
var comp_after_upload = document.getElementById("comp_after_upload")
var ori_before_upload = document.getElementById("ori_before_upload")
var ori_after_upload = document.getElementById("ori_after_upload")

function comp_uploaded(file)
{
    comp_before_upload.style.display = "none";
    comp_after_upload.style.display = "block";
    document.getElementById("comp_filename").innerHTML = file.files[0].name;
}

function ori_uploaded(file)
{
    ori_before_upload.style.display = "none";
    ori_after_upload.style.display = "block";
    document.getElementById("ori_filename").innerHTML = file.files[0].name;
}



// Get the modal
var modal = document.getElementById("id-functions");
var submitBtn = document.getElementById("id-submit-btn");
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

$(document).ready(function() {
  $('.js-example-basic-multiple').select2();
});