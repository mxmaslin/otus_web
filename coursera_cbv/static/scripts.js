$(function() {
    $("#generate_forms").click(function() {

    
        quantity = $("[name=quantity]").val();
        $("[name=form-TOTAL_FORMS]").val(quantity);
        for (i=0; i < quantity; i++) {
            html = $("#form_template").clone().html().replace('/__prefix_/g', i);
            $("#forms").append(html);
        };
     })
})
