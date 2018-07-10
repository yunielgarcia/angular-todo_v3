'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo) {

  $scope.deleteTodo = deleteTodo;
  $scope.createTask = createTask;
  $scope.updateTask = updateTask;

  function createTask(todo) {
      todo.$save();
  }

  function updateTask(todo) {
      Todo.update(todo);
  }

  function deleteTodo(todo, index) {
    $scope.todos.splice(index, 1);
    Todo.delete({id: todo.id});
  }
});