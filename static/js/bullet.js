BRAIN.Bullet = (function() {
	var newBullet = function(id, x, y, team, vx, vy, direction) {
		var unit = {
			x : x,
			y : y,
			direction : BRAIN.defaultTo(direction, 0),
			vx : BRAIN.defaultTo(vx, 0),
			vy : BRAIN.defaultTo(vy, 0),
			id : id,
			team : BRAIN.defaultTo(team, 0),
			hidden : false,
			dead : false,
		};
		if (direction == undefined && vx != undefined && vy != undefined) {
			unit.direction = Math.atan2(vy, vx);
		}
		return unit;
	};

	var getBullet = function(id) {
		for (var i = 0; i < BRAIN.bullets.length; i++) {
			if (BRAIN.bullets[i].id == id) {
				return BRAIN.bullets[i];
			}
		}
		return undefined;
	};

	var removeBullet = function(id) {
		for (var i = 0; i < BRAIN.bullets.length; i++) {
			if (BRAIN.bullets[i].id == id) {
				BRAIN.bullets.splice(i, 1);
			}
		}
	};

	return {
		newBullet : newBullet,
		getBullet : getBullet,
		removeBullet : removeBullet,
	};
})();
