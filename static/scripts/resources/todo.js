'use strict';

angular.module('todoListApp')
    .factory('Todo', function ($resource) {

        /** For the angularjs app to feed from the api resources it has to provide a toke that can be obtain at  '/api/v1/users/token' with basic credentials.
         After getting the token replace the token value in the service.
         This is not the ideal way usually this is done providing the token as a response for login maybe and handle it in the frontend app.
         I think is not required for the project to pass.
         Thanks. */

            // REPLACE token WITH YOUR OWN TOKEN TO TEST THE ANGULAR APP

        var token = 'eyJpYXQiOjE1MzE5MjA3NDgsImV4cCI6MTUzMTkyNDM0OCwiYWxnIjoiSFMyNTYifQ.eyJpZCI6MX0.C4_L8efLiK7TQc8HxUAhwc1FJqz66M535h_-7HIMDN8'
        return $resource('/api/v1/todos/:id', {id: '@id'}, {
            update: {
                method: 'PUT',
                headers: {
                    'Authorization': 'Token ' + token
                }
            },
            get: {
                method: 'GET',
                isArray: false,
                headers: {
                    'Authorization': 'Token ' + token
                }
            },
            delete: {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Token ' + token
                }
            },
        });
    });