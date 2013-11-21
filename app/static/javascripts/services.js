angular.module('dccAdminServices', ['ngResource'])
        .factory('Users', function($resource) {
                return $resource('/api/user/', {}, {
                        query: {
                                method: 'GET',
                                isArray: true
                        }
                });
        });
