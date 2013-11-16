angular.module('dccAdmin', ['angularFlaskServices'])
        .config(['$routeProvider', '$locationProvider',
                function($routeProvider, $locationProvider) {
                $routeProvider
                .when('/', {
                        templateUrl: 'static/partials/index.html',
                        controller: IndexController
                })
                .otherwise({
                        redirectTo: '/'
                })
                ;

                $locationProvider.html5Mode(true);
        }])
;