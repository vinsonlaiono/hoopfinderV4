// IIFE to get all reviews for user in session
(() => {
    console.log("Loaded Users ajax page")
    console.log("User id: ", $('#user_id').val())
    
    var url = "/reviews/"+$('#user_id').val() + "/all_reviews";
    console.log(url + "===========================================================================")
    $.ajax({
        method: "GET",
        url: url,
      })
        .done(function( data ) {
            console.log("In done route for sure in IIFE")
            $('.reviews').html(data)
        });
        // MAKE A REQUEST TO THE SERVER TO REFRESH THE PAGE EVERY 2 SECONDS! !- HORRIBLE IDEA NEED DJANGO CHANNELS FOR SOCKETS-!
        // (() => {
        //   setInterval(function(){
        //     $.ajax({
        //       method: "GET",
        //       url: url,
        //     })
        //       .done(function( data ) {
        //           console.log("In done route for sure in IIFE")
        //           $('.reviews').html(data)
        //       });
        //     }, 2000);
        // })()
        
})();



// ============ TASK =============
// Create a listener to watch for a scroll to the bottom of the page to load more reviews