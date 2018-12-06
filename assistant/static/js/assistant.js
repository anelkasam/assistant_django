$('#generate_token').click(function () {
    $.get('/auth/create_token/', function (data) {
        $('#token').replaceWith("<p>" + data + "</p>");
    });
});

function toggle(table_id) {
    var x = document.getElementById(table_id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
