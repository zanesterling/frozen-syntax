BRAIN.Wall = (function() {
	var newWall = function(id, x, y, width, height) {
		var wall = {
			x : x,
			y : y,
			id : id,
            width: width,
            height: height
		};
		return wall;
	};

	var getWall = function(id) {
		for (var i = 0; i < BRAIN.walls.length; i++) {
			if (BRAIN.walls[i].id == id) {
				return BRAIN.walls[i];
			}
		}
		return undefined;
	};

	var removeWall = function(id) {
		for (var i = 0; i < BRAIN.walls.length; i++) {
			if (BRAIN.walls[i].id == id) {
				BRAIN.walls.splice(i, 1);
			}
		}
	};

	return {
		newWall : newWall,
		getWall : getWall,
		removeWall : removeWall,
	};
})();
