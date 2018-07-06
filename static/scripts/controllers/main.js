'use strict';

angular.module('todoListApp')
.controller('mainCtrl',['$scope', 'Todo', function($scope, Todo){
  
  $scope.todos = Todo.query().$promise
        .then(function (response) {
        // do something with the response
            return response.data
        }, function (error) {
            // pass the error the the error service
            console.log('error')
            return []
        });;
  
  $scope.addTodo = function() {
    var todo = new Todo();
    todo.name = 'New task!'
    todo.completed = false;
    $scope.todos.unshift(todo);
  };
  
}])