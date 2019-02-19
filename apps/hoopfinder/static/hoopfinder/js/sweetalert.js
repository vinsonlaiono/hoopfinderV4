

$(document).ready(function () {
    $('#login').click(function () {
        swal.fire({
            title: "Log in",
            text: "Do you want to login",
            button: {
                cancel: true,
                confirm: "Log in"
            }
        })
        console.log("This is the function vinson ")
    })
})