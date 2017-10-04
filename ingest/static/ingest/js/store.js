(function() {
    'use strict';

    // Container area
    var content = window.content;

    // Repository sub views
    var views = new Map();

    // Utilities module
    var utils = Utils;

    var repositories = $('.repository');

    repositories.on('click', getContents);

    function getContents(event) {
        var id = event.target.getAttribute('data-repo-id');
        console.log(event.target)
        $.get("/archiva/content/id=" + id)
           .done(function(response) {
              views.set(id, response);
              content.html(response);
        }).fail(function(errorResponse) {
            console.log(errorResponse);
        });
    }

    function displayView(viewId) {
        views.set(viewId, content.html());
        alert(views.get(viewId));
    }

}())