angular.module('dccAdminServices', ['ngResource'])
        .factory('Users', function($resource) {
                return $resource('/api/user/');
        })
        .factory('Roles', function($resource) {
                return $resource('/api/role/');
        });
