$(document).ready( function() {
    $('#hide').click( function () {
      if (parseInt($(".jedna-afera").css("height").replace("px",'')) > 150) {  
        $('.wydarzenie-aktorzy,.opis,.wydarzen').toggle(200,'linear');
        $(".jedna-afera").css("height","10ex");
      } else {
        $(".jedna-afera").css("height","48ex"); 
        $('.wydarzenie-aktorzy,.opis,.wydarzen').toggle(200,'linear');
      }
    } )
} );
