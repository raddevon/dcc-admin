angular.module('angularFlaskServices', ['ngResource'])
        .factory('Users', function($resource) {
                return $resource('/api/users/', {}, {
                        query: {
                                method: 'GET',
                                isArray: true
                        }
                });
        })
;