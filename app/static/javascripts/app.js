angular.module('dccAdmin', ['angularFlaskServices'])
        .config(['$routeProvider', '$locationProvider',
                function($routeProvider, $locationProvider) {
                $routeProvider
                .when('/', {
                        templateUrl: 'static/partials/index.html',
                        controller: IndexController
                })
                .when('/users', {
                        templateUrl: 'static/partials/users.html',
                        controller: userManagementController
                })
                .otherwise({
                        redirectTo: '/'
                })
                ;

                $locationProvider.html5Mode(true);
        }]);