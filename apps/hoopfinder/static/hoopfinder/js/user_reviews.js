$(document).ready(() => {
    console.log("In follow.js file")

    // HANDLE FOLLOW AND UNFOLLOW OF USERS
    let follow_user = (followed_id, follower_id) => {
        
        var url = `/followAPI/${followed_id}/${follower_id}`
        console.log(`user id: ${follower_id} is following userid: ${followed_id}`)
        console.log("URL: "+ url)
        $.ajax({
            url: url,
            method: 'GET',
        }).done((res) => {
            if(res){

              console.log('Success in following api route')
            }
            
          })
    }

    // GET ALL REVIEWED THAT BELONG TO THE CURRENT USER IN SESION
    let getMyFeedReviews = (feedType) => {
        
        var url = "/reviews/"+$('#user_id').val() + "/" + feedType;
        console.log("***************Getting my reviews" + url)
        $.ajax({
            method: "GET",
            url: url,
          })
            .done(function( data ) {
                console.log("In ajax route to get users reviews")
                $('.reviews').html(data)
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'center',
                    showConfirmButton: false,
                    timer: 3000
                  });
                  Toast.fire({
                    type: 'success',
                    title: 'You are now viewing ' + feedType
                  })
            });

    }

    // FUNCTIONS FOR LISTENERS
    $('.follow_button').click(function () {
        var followed_id = $(this).attr('followedID')
        var follower_id = $(this).attr('followerID')
        follow_user(followed_id, follower_id);
        const Toast = Swal.mixin({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        });
        Toast.fire({
          type: 'success',
          title: 'Followed User'
        })
        $(this).html('<span class="fa fa-user-plus mr-2"></span> Unfollow')

    })
    $('.my_feed').click( function() {
        let feedType = $(this).attr('feedType')
        getMyFeedReviews(feedType);
    })
})