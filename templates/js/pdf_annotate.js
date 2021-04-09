var d = new Date().getTime();
        console.log(d);
        // document.getElementById("comp").src = "viewer/web/viewer.html?file=comp.pdf?rnd=" + d;
        document.getElementById("ori").src = "viewer/web/annotate_original.html?file=ori.pdf?rnd=" + d;
        document.getElementById("comp").src = "viewer/web/annotate_compare.html?file=comp.pdf?rnd=" + d;
      
        $(document).ready(function(){


        $(window.frames[0]).on('scroll', function() {
        $(window.frames[1]).scrollTop($(window.frames[0]).scrollTop());
        });

        $(window.frames[1]).on('scroll', function() {
        $(window.frames[0]).scrollTop($(window.frames[1]).scrollTop());
        });

        });

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

// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

var navbar = document.getElementById("id_topnav");
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}

// Get the modal
var modal = document.getElementById("myModal");
// Get the button that opens the modal
var helpBtn = document.getElementById("id-help-button");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
helpBtn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function start_ocr()
{

var saveTemplate = confirm("Do you want to save the current marked regions as template");

if (saveTemplate == true){
  var tmpName = prompt("Please enter the template name");
  if (tmpName!= null){
    $.post("/saveTmp",{'tmpName': tmpName}).done(function(data){
    }).fail(function(){});
  }
}



document.getElementById('upload_page').style.display = "none";
document.getElementById('loading_page').style.display = "flex";
}

$("#comp").on('load', function(){
  document.getElementById('comp').contentWindow.PDFViewerApplication.pdfViewer.currentPageNumber = 1;
  $("#comp").contents().find("#viewerContainer").on('scroll', function(){ 
    $("#ori").contents().find("#viewerContainer").scrollTop($(this).scrollTop());
  });
  
  });
  
  $("#ori").on('load', function(){
  $("#ori").contents().find("#viewerContainer").on('scroll', function(){ 
   $("#comp").contents().find("#viewerContainer").scrollTop($(this).scrollTop());
   });
  });
