$('#add_lesson').click(function() {
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#add_lesson_formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});