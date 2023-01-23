$(document).ready(function() {
        
    $("#driver").click(function(event){
       $.getJSON('/media/andrii/E83219FE3219D284/DeepFaceLab/DeepFaceLab_Linux/DeepFaceLab/progr_bar.json', function(jd) {
          $('#stage').html('<p> Name: ' + jd.total + '</p>');
          $('#stage').append('<p>Age : ' + jd.current+ '</p>');
       });
    });
       
 });