(function () {
    var app = angular.module('staticBase', []);

    app.directive('baseContent', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/html/base/base_content.html'
        }
    });
    app.directive('baseHome', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/html/base/base_idea.html'
        }
    });
    app.directive('baseAbout', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/html/base/base_prototype.html'
        }
    });
    app.directive('baseContact', function () {
        return {
            restrict: 'E',
            templateUrl: '/static/html/base/base_contact.html'
        }
    });

    app.controller('BaseNavController', function () {
        this.nav = 1;
        this.selectNav = function (setNav) {
            this.nav = setNav;
        };
        this.isSelected = function (checkNav) {
            return this.nav === checkNav;
        };
    });
})();

$(document).on("click", "#toggle-signIn", function () {
    $("#signUpModal").modal('hide');
    $("#signInModal").modal('show');
});

$(document).on("click", "#toggle-signUp", function () {
    $("#signInModal").modal('hide');
    $("#signUpModal").modal('show');
});