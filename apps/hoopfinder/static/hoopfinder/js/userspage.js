$(document).ready( () => {
    console.log("Loaded Users ajax page")
    console.log("User id: ", $('#user_id').val())
    var url = "/reviews/"+$('#user_id').val();
    $.ajax({
        method: "GET",
        url: url,
      })
        .done(function( data ) {
            console.log("In done route")
            console.log(data)
            $('.reviews').html(data)
        });
});