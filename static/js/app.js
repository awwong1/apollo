(function () {
    var app = angular.module('apollo', []);
    app.directive('application', function(){
        return {
            restrict: 'E',
            templateUrl: '/static/html/application.html'
        }
    });
})();