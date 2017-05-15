$('#remove_entity').click(function () {
    $('#del_entity').val("Delete")
});

$('#existing_entity_table').click(function () {
    var source = $(this)
    var name = source.find("#name").html()
    var desc = source.find("#description").html()
    $('#placeableName').val(name)
    $('#new_description').val(desc)
})