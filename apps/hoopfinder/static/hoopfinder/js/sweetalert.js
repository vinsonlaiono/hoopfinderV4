

$(document).ready(function () {
    // Use ajax to delete a single review
    $('.delete_review').click(function () {
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
                    Swal.fire(
                      'Deleted!',
                      'Your file has been deleted.',
                      'success'
                    )
                })
            }
          })
        console.log("This is the function vinson ")
    })
})