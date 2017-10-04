/**
 * Utility functions used through out the app
 */
 var Utils = (function(jQuery) {
    'use strict';

    /**
     * Gets the user id from the url string
     * @param url: string the url string parameter
     */
     function getUserId(url) {
       if(typeof url !== 'string')
            return "";
       return url.slice(-1);
     }

     /**
      * Updates the view with the given id. This function should
      * be called when a post request that alters the state of the database
      * is made. For example when a new Repository is created.
      */
      function updateView(url, id, map, render) {
        var render = render
        if(typeof url !== 'string' || typeof id !== 'string' || !(map instanceof Map))
            throw new Error('Check parameters');

        $.get(url, function(viewData) {
            map.set(id, viewData);
            if (render === true)
                renderView(id, map, window.content);
        });
      }

      /**
       * Refreshes the view with the given id and initializes all event handlers
       * for the view. This should be called after update view so that the contents
       * retrieved can be rendered on the page.
       */
       function renderView(id, map, container) {
            container.html(map.get(id));
            setupUIComponents();
       }

      /**
       * Initializes the UI components (checkboxes, dropdowns etc.)
       */
       function setupUIComponents() {
          var dropdowns = $('.dropdown'),
              checkboxes = $('.checkbox'),
              radios = $('.radios');

          if(dropdowns.val() !== undefined)
              dropdowns.dropdown();

          if(checkboxes.val() !== undefined)
              checkboxes.checkbox();
        }

      /**
       *
       */
       function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

     /**
      *
      */
      function csrfSafeMethod(method) {
          // these HTTP methods do not require CSRF protection
          return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      }

      /**
       * Builds a table given some data. it uses the data's keys
       * as column names
       */
       function buildTable(data) {
            var newTable = $('</table>', {
                'class': 'files-table'
            });
       }

     /**
      * Public API
      */
      return {
           'getUserId': getUserId,
           'getCookie': getCookie,
           'updateView': updateView,
           'renderView': renderView,
           'setupUIComponents': setupUIComponents,
           'csrfSafeMethod': csrfSafeMethod };
 }(jQuery));