$(function() {
    'use strict';

    /////////////////////////////////////////////
    ////     PUBLIC ACCESS VARIABLES         ////
    /////////////////////////////////////////////

    // The frame where all html content is injected
    window.content = $('#content');

    // This Map stores the views in the application
    window.views = new Map();

    /////////////////////////////////////////////
    ////    PRIVATE VARIABLES                ////
    /////////////////////////////////////////////

    // Stores a reference to the utilities module
    var utils = Utils;

    // Control buttons that link to separate views
    var btnLinks = null;

    // Home view cards that link to specific views
    var cardLinks = null;

    // Urls specifying all views in the application
    var urls = {
        home: "/archiva/dashboard/home/id=" + utils.getUserId(window.location.href),
        ingest: "/archiva/dashboard/ingest/id=" + utils.getUserId(window.location.href),
        store: "/archiva/dashboard/store/id=" + utils.getUserId(window.location.href),
        search: '/archiva/dashboard/search/id=' + utils.getUserId(window.location.href)
    };

    // Endpoint APIs
    var endpoints = {
        getallrepositories: "",
        findcontent: ""
    };

    /**
     * Initializes the application
     */
    function init() {
        // Load all application views
        $.when(
            // Get the home view
            $.get(urls.home)
              .done(function(data) {
                //console.log(data);
                views.set('1', data);

            }),

            // Get the ingest view
            $.get(urls.ingest)
              .done(function(data) {
                views.set('2', data);
            }),

            // Get the ingest view
            $.get(urls.store)
              .done(function(data) {
                views.set('3', data);
            }),

            // Get the search view
            $.get(urls.search)
              .done(function(data) {
                views.set('4', data);
            })
        ).then(function() {
            // Since this will be the first view a user sees
            // load it first.
            content.html(views.get('1'));
        });
    }

    function setupEventHandlers() {
        // Get all navigation links and register events for them
        btnLinks = $('.btn').on('click', function(event) {
            event.preventDefault();
            btnLinks.removeClass('actives');
            $(this).addClass('actives');

            content.html(views.get(event.target.getAttribute('data-id')));
            utils.setupUIComponents();
        });
    }

    // Display the loader when an ajax request is set
    $(document).ajaxStart(function() {
        $('#loader').show();
    });

    // Hide the loader as soon as the ajax request is finished
    $(document).ajaxStop(function() {
        $('#loader').hide();
        $('#content').show();
    });

    // Creates a modal view
    function openCreateModal() {
        //$('.ui.modal').modal('show');
    }

    init();
    setupEventHandlers();
});