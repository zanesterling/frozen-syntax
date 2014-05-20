BRAIN.Unit = (function() {
	var newUnit = function(id, x, y, team, vx, vy, direction) {
		var unit = {
			x : x,
			y : y,
			direction : BRAIN.defaultTo(direction, 0),
			vx : BRAIN.defaultTo(vx, 0),
			vy : BRAIN.defaultTo(vy, 0),
			id : id,
			team : BRAIN.defaultTo(team, 0),
			hidden : false,	
		};
		if (direction == undefined && vx != undefined && vy != undefined) {
			unit.direction = Math.atan2(vy, vx);
		}
		return unit;
	};

	var getUnit = function(id) {
		for (var i = 0; i < BRAIN.units.length; i++) {
			if (BRAIN.units[i].id == id) {
				return BRAIN.units[i];
			}
		}
		return undefined;
	};

	var removeUnit = function(id) {
		for (var i = 0; i < BRAIN.units.length; i++) {
			if (BRAIN.units[i].id == id) {
				BRAIN.units.splice(i, 1);
			}
		}
	};

	return {
		newUnit : newUnit,
		getUnit : getUnit,
		removeUnit : removeUnit,
	};
})();
