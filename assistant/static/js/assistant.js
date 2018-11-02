$('#generate_token').click(function () {
    $.get('/auth/create_token/', function (data) {
        $('#token').replaceWith("<p>" + data + "</p>");
    });
});
