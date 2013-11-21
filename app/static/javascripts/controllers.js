function userManagementController($scope, $http, Users) {
    var usersQuery = Users.get({}, function(users) {
        $scope.users = users.objects;
    });
}

function indexController($scope) {
    $scope.currentUser = 'raddevon@gmail.com';
}
