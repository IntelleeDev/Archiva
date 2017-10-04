(function() {
    'use strict';

    // modal for entering meta tags
    var metaModal = $('.ui.modal');

    // file reader object
    var fileReader = new FileReader();

    // reference to the utils module
    var utils = Utils;

    // file upload form
    var fileUploadForm = $('#file-upload-form');

    // file input field
    var fileInputField = $('#file');

    var createBtn = $('#create');

    // upload file button
    var uploadBtn = $('#upload-btn');

    // file dialog button
    var fileDialogBtn = $('#file-btn');

    createBtn.on('click', createRepository);
    uploadBtn.on('click', uploadFiles);

    $('.show-area').hide();
    $('.progress-track').hide();

    // setup handler for the file button
    fileDialogBtn.on('click', function() {
        fileInputField.click();
        processFileUpload();
    });

    // setup handler for file input
    fileUploadForm.on('change', processFileUpload);

    /**
     * Sends a post to the server to create a repository
     */
    function createRepository(event) {
        event.preventDefault();
        $.post('/archiva/repository/create/id='+utils.getUserId(window.location.href), $("#create-form").serialize())
            .done(function(data) {
                //alert(data);
                // update the ingest view
                utils.updateView("/archiva/dashboard/ingest/id=" + utils.getUserId(window.location.href),
                    "2", window.views, true);

                // render the current view on the page
                utils.renderView("2", window.views, window.content);

                // update the store view
                utils.updateView("/archiva/dashboard/store/id=" + utils.getUserId(window.location.href),
                    "3", window.views);
            })
            .fail(function(data) {
                console.log(data);
            });
    }

    /**
     * We want to send the csrfTOKEN header only for POST requests
     */
    function setupAjax() {
       var csrftoken = utils.getCookie("csrftoken");
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!utils.csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }
    setupAjax();

    /**
     * Gets the files the user wants to upload and displays them
     */
     function processFileUpload(event) {
        var files = event.target.files;

        var f = files[0];  // gets the first file

        // Setup event handler for file reader
        fileReader.addEventListener('load', function(event) {
            $('.upload-area').hide();
            $('.show-area').show();

            var allowed = ['pdf', 'txt', 'zip', 'rar'];

            $('#filename').html(" "+f.name);
            $('#size').html(" "+f.size+"MB");
            $('#type').html(" "+f.type);

        }, false);

        fileReader.readAsText(f);
     }

     /**
      * Show meta form page
      */
      function showMetaFormPage() {
         utils.setupUIComponents();
         metaModal.modal('show');
      }

     /**
      * Uploads the selected files
      */
      function uploadFiles(event) {
        event.preventDefault();
        metaModal.modal({
            closable: false,
            autofocus: true
         });
         metaModal.modal('show');
        showMetaFormPage();
        var click = 1;

        $('#save').on('click', function() {
            if (click > 1)
                return;
            metaModal.modal('hide');
            $('.ingest').fadeOut(500);
            $('#tracker').html('Ingest status report')
            ++click;

            var formData = new FormData(document.getElementById('file-upload-form'));
            var repoName = $('.ui.radio.checked > input').val();
            formData.append('title', repoName);
            formData.append('tags', $('#tag').val());
            formData.append('desc', $('#desc').val());


            // wait a while befor iniating ajax call we initiate and ajax call
            setTimeout(function() {
                $.ajax({
                    url: "/archiva/dashboard/ingest/id=" + utils.getUserId(window.location.href),
                    method: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false
                })
                .done(function(response) {
                    alert(response);
                    $('.progress-track').fadeIn(500);
                })
                .fail(function(response) {
                    console.log(response);
                });
            }, 3000);
        })

      }
}());