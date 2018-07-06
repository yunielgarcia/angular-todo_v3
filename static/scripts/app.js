'use strict';

angular.module('todoListApp', ['ngResource'])
.config(['$qProvider', function ($qProvider) {
    $qProvider.errorOnUnhandledRejections(false);
}]);
