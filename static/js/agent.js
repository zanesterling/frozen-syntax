BRAIN.Agent = (function() {
	var newAgent = function(id, x, y, team, vx, vy, direction) {
		var agent = {
			x : x,
			y : y,
			direction : BRAIN.defaultTo(direction, 0),
			vx : BRAIN.defaultTo(vx, 0),
			vy : BRAIN.defaultTo(vy, 0),
			id : id,
			team : BRAIN.defaultTo(team, 0),
		};
		if (direction == undefined && vx != undefined && vy != undefined) {
			agent.direction = Math.atan2(vy, vx);
		}
		return agent;
	};

	var getAgent = function(id) {
		for (var i = 0; i < BRAIN.agents.length; i++) {
			if (BRAIN.agents[i].id == id) {
				return BRAIN.agents[i];
			}
		}
		return undefined;
	};

	var removeAgent = function(id) {
		for (var i = 0; i < BRAIN.agents.length; i++) {
			if (BRAIN.agents[i].id == id) {
				BRAIN.agents.splice(i, 1);
			}
		}
	};

	return {
		newAgent : newAgent,
		getAgent : getAgent,
		removeAgent : removeAgent,
	};
})();
