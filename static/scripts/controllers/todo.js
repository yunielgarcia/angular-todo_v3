'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo) {

  $scope.deleteTodo = function(todo, index) {
    $scope.todos.splice(index, 1);
    todo.$delete();
  };
  
  $scope.saveTodos = function() {
    var filteredTodos = $scope.todos.filter(function(todo){
      if(todo.edited) {
        return todo;
      }
    });
    filteredTodos.forEach(function(todo) {
      if (todo.id) {
        Todo.update(todo);
      } else {
        todo.$save();
      }
    });
  };

  $scope.createTask = createTask;
  $scope.updateTask = updateTask;

  function createTask(todo) {
      todo.$save();
  }

  function updateTask(todo) {
      Todo.update(todo);
  }
});