function userManagementController($scope, $http, Users, Roles) {
    var usersQuery = Users.get({}, function(users) {
        $scope.users = users;
    });
    var rolesQuery = Roles.get({}, function(roles) {
        $scope.roles = roles;
    })
}

function indexController($scope) {
    $scope.currentUser = 'raddevon@gmail.com';
}
