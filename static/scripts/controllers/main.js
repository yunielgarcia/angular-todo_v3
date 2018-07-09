'use strict';

angular.module('todoListApp')
    .controller('mainCtrl', ['$scope', 'Todo', function ($scope, Todo) {

        $scope.todos = [];


        $scope.addTodo = function () {
            var todo = new Todo();
            todo.name = 'New task!'
            todo.completed = false;
            // $scope.todos.unshift(todo);
            console.log('angular working')
        };

        function fetchAll() {
            Todo.get().$promise
                .then(function (data) {
                    // do something with the response
                    $scope.todos = data.todos;
                }, function (error) {
                    // pass the error the the error service
                    console.log(error)
                    return []
                });
        }

        //Execute
        fetchAll();
    }]);