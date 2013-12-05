function userManagementController($scope, $http, Users, Roles) {
    var usersQuery = Users.get({}, function(users) {
        $scope.users = users;

        // Selects current user roles
        for (var key in $scope.users) {
            var user = $scope.users[key];
            user.selectedRoles = [];
            for (var roleKey in user.roles) {
                user.selectedRoles.push(String(user.roles[roleKey].id));
            }
        }

    });
    var rolesQuery = Roles.get({}, function(roles) {
        $scope.roles = roles;
    });
}

function indexController($scope) {
    $scope.currentUser = 'raddevon@gmail.com';
}
