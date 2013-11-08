var renderNewContent = function(template, context) {
    var source = $(template).html();
    var template = Handlebars.compile(source);
    var output = template(context);

    $('#main-content').html(output);
};

var getNewContent = function(apiEndpoint) {
    $.ajax({
        type: 'GET',
        url: apiEndpoint,
        dataType: 'json',
        // Not sure how to send authentication to the server.
        // Even if I can figure out how, I'm not sure how to send it
        // without including it in plain text inside the JavaScript.
        headers: '',
        success: function(data) {
            renderNewContent('#user-management-template', data);
        }
    })
};

$('#user-management-link').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    getNewContent('/api/users/');
    return false;
});
