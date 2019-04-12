$(document).ready(() => {
    $.ajax({
        url: "/ajax_courts",
        method: "GET",
    })
    .done((data) => {
        $('#all_courts').html(data)
    })
    
    $('.addCourt').click(function() {
        const {value: formValues} = Swal.fire({
            title: 'Add a new court',
            html:
                // <form action="/add_court" method="post">
                    '<div class="form-group">'+
                        '<input id="swal-input1" type="text" class="swal2-input" name="court_name" placeholder="Name">'+
                    '</div>'+
                    '<div class="form-group">'+
                        '<input id="swal-input2" type="text" class="swal2-input" name="address" placeholder="Address">'+
                    '</div>'+
                    '<div class="form-group">'+
                            '<input id="swal-input3" type="text" class="swal2-input" name="city" placeholder="City">'+
                    '</div>'+
                    '<div class="form-group">'+
                            '<input id="swal-input4" type="text" class="swal2-input" name="state" placeholder="State">'+
                    '</div>'+
                    '<div class="form-group">'+
                            '<input id="swal-input5" type="text" class="swal2-input" name="zipcode" placeholder="Zipcode">'+
                    '</div>'+
                    '<div class="form-group">'+
                            '<input id="swal-input6" type="text" class="swal2-input" name="imagelink" placeholder="image url">'+
                    '</div>',
                   
                // </form>,
            //   '<input id="swal-input1" class="swal2-input">' +
            //   '<input id="swal-input2" class="swal2-input">',
            focusConfirm: false,
            preConfirm: () => {
                return [
                  document.getElementById('swal-input1').value,
                  document.getElementById('swal-input2').value,
                  document.getElementById('swal-input3').value,
                  document.getElementById('swal-input4').value,
                  document.getElementById('swal-input5').value,
                  document.getElementById('swal-input6').value,
                ]
              }
          })
          
          if (formValues) {
            Swal.fire(json.stringify(formValues))
          }
    })
})

