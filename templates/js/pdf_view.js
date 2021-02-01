var d = new Date().getTime();
console.log(d);
document.getElementById("comp").src = "viewer/web/viewer.html?file=comp_final.pdf?rnd=" + d;
document.getElementById("ori").src = "viewer/web/viewer.html?file=ori_final.pdf?rnd=" + d;
$('#upload_tab').attr('disabled','disabled');
$('#annotate_tab').attr('disabled','disabled');

$(window).on('load', function(){
  $(".comparison_report").hide();
  $(".extraction_view").hide();
  $(".report_subTab").hide();

  $("#report_tab").click(function(){
    $(".report_subTab").toggle();
  });

  $("#full_view_tab").click(function(){
    $(".comparison_report").hide();
    $(".full_view").show();
  });

  $("#comparison_report_tab").click(function(){
    $(".full_view").hide();
    $(".extraction_view").hide();
    $(".comparison_report").show();
  });


  $("#extract_tab").click(function(){
    $(".full_view").hide();
    $(".comparison_report").hide();
    $(".extraction_view").show();
  });

  $(window.frames[0]).on('scroll', function() {
    $(window.frames[1]).scrollTop($(window.frames[0]).scrollTop());
  });

  $(window.frames[1]).on('scroll', function() {
    $(window.frames[0]).scrollTop($(window.frames[1]).scrollTop());
  });
  
  $('.js-example-basic-multiple').select2();
  $('.extract_table').DataTable();  

  $(".page").click(function(){
    var page = Number($(this).find('a').attr('class'));
    document.getElementById('comp').contentWindow.PDFViewerApplication.pdfViewer.currentPageNumber = page;
    $("#full_view_tab").click();
  
  })

  $( "<div>Extraction Result</div>" ).insertBefore( "#DataTables_Table_0_wrapper" );
  $('#DataTables_Table_0_wrapper').prev('div').addClass('table-title');
  $('#extract_table tbody').on( 'mouseenter', 'td', function () {
      var colIdx = table.cell(this).index().column;

      $( table.cells().nodes() ).removeClass( 'highlight' );
      $( table.column( colIdx ).nodes() ).addClass( 'highlight' );
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

$("#comp").on('load', function(){

  $("#comp").contents().find("#viewerContainer").on('scroll', function(){ 
    $("#ori").contents().find("#viewerContainer").scrollTop($(this).scrollTop());
  });
  
  });
  
  
  $("#ori").on('load', function(){
  $("#ori").contents().find("#viewerContainer").on('scroll', function(){ 
   $("#comp").contents().find("#viewerContainer").scrollTop($(this).scrollTop());
   });
  });
