function userManagementController($scope, $http) {
    var usersQuery = Users.get({}, function(posts) {
        $scope.users = users.objects;
    });
}

function indexController($scope) {

}
