angular.module('dccAdmin', ['ngRoute', 'dccAdminServices'])
        .config(['$routeProvider', '$locationProvider',
                function($routeProvider, $locationProvider) {
                $routeProvider
                .when('/', {
                        templateUrl: 'static/partials/home.html',
                        controller: indexController
                })
                .when('/users', {
                        templateUrl: 'static/partials/users.html',
                        controller: userManagementController
                })
                .otherwise({
                        redirectTo: '/'
                });

                $locationProvider.html5Mode(true);
        }]);
