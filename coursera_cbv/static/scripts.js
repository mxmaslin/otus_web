$(function() {
    $("#generate_forms").click(function() {
        html = $("#form_template").clone().html().replace('/__prefix_/g', 1);
        $("#forms").append(html);
     })
})
