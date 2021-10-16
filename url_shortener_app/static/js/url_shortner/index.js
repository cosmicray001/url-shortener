$(document).ready(function () {
    $("#url-form").validate({
        rules: {
            main_url: {
                required: true,
                url: true
            }
        }
    });
    $(document).on('click', '#copy-url', function () {
        var temp = $("<input>");
        $("body").append(temp);
        temp.val($('#result').val()).select();
        document.execCommand("copy");
        temp.remove();
        toastr.success("Copied to clipboard successfully");
    });
    $(document).on('click', '#redirect', function(){
        window.location = $('#result').val();
    })
});