  // Delete a review  
  // $('.delete_review').click(function () {
    $('.delete_review').on('click',  function(){
        console.log("Fired with click in DOM created tag")
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
          }).then((result) => {
            console.log(result)
            console.log($(this).attr('url'))
            if (result.value) {
                $.ajax({
                    url: $(this).attr('url'),
                    method: "GET"
                }).done(() => {
                    const Toast = Swal.mixin({
                      toast: true,
                      position: 'top-end',
                      showConfirmButton: false,
                      timer: 3000
                    });
                    
                    Toast.fire({
                      type: 'success',
                      title: 'Successfully deleted'
                    })
                })
            }
          })
        console.log("This is the function vinson ")
    })
    // Set the profile picture the github username image
    $('.profile_picture').click(function() {
      console.log("Images Clicked")
      Swal.fire({
          title: 'Submit your Github username',
          input: 'text',
          inputAttributes: {
            autocapitalize: 'off'
          },
          showCancelButton: true,
          cancelButtonColor: '#d33',
          confirmButtonText: 'Look up',
          showLoaderOnConfirm: true,
          preConfirm: (login) => {
            return fetch(`//api.github.com/users/${login}`)
              .then(response => {
                if (!response.ok) {
                  throw new Error(response.statusText)
                }
                return response.json()
              })
              .catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          },
          allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
          if (result.value) {
            Swal.fire({
              title: `${result.value.login}'s avatar`,
              imageUrl: result.value.avatar_url
            })
          }
          $(this).attr('src', result.value.avatar_url)
      })
    });