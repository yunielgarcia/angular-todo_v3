'use strict';

angular.module('todoListApp')
    .factory('Todo', function ($resource) {
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