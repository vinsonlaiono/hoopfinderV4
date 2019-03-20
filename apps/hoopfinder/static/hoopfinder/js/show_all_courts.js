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
                `<form action="/add_court" method="post">
                        <div class="form-group">
                            <input type="text" class="swal2-input" name="court_name" placeholder="Name">
                        </div>
                        <div class="form-group">
                            <input type="text" class="swal2-input" name="address" placeholder="Address">
                        </div>
                        <div class="form-group">
                                <input type="text" class="swal2-input" name="city" placeholder="City">
                        </div>
                        <div class="form-group">
                                <input type="text" class="swal2-input" name="state" placeholder="State">
                        </div>
                        <div class="form-group">
                                <input type="text" class="swal2-input" name="zipcode" placeholder="Zipcode">
                        </div>
                        <div class="form-group">
                                <input type="text" class="swal2-input" name="imagelink" placeholder="image url">
                        </div>
                        <!-- <div class="custom-file">
                            <input type="file" class="custom-file-input" name="validatedCustomFile" required>
                            <label class="custom-file-label" for="validatedCustomFile">Choose file...</label>
                        </div> -->
                    </form>`,
            //   '<input id="swal-input1" class="swal2-input">' +
            //   '<input id="swal-input2" class="swal2-input">',
            focusConfirm: false
          })
          
          if (formValues) {
            Swal.fire(json.stringify(formValues))
          }
    })
})

