$(function() {
    $("#generate_forms").click(function() {
        html = $("#form_template").clone().html();
        $("#forms").append(html);
     })
})
