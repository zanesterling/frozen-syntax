BRAIN.Agent = (function() {
	var newAgent = function(x, y, team, direction, vx, vy) {
		return {
			x : x,
			y : y,
			direction : BRAIN.defaultTo(direction, 0),
			vx : BRAIN.defaultTo(vx, 0),
			vy : BRAIN.defaultTo(vy, 0),
			id : 0,
			team : BRAIN.defaultTo(team, 0),
		};
	};

	return {
		newAgent : newAgent,
	};
})();
