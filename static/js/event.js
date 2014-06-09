BRAIN.Event = (function() {
	var newEvent = function(type, id, timestamp, props) {
		return {
			type : type,
			id : id,
			timestamp : timestamp,
			props : props
		};
	};

	var runEvent = function(e) {
		b = e;
		if (e.type == "ActorSpawned") {
            if (e.data.type == "Unit") {
                var unit = BRAIN.Unit.newUnit(e.data.typeID, e.data.x, e.data.y, e.data.team);
                BRAIN.units.push(unit);
            } else if (e.data.type == "Bullet") {
                var bullet = BRAIN.Bullet.newBullet(e.data.typeID, e.data.x, e.data.y, e.data.team);
                BRAIN.bullets.push(bullet);
            }
		} else if (e.type == "ActorTrajectoryUpdate") {
			var unit;
            if (e.data.type == "Unit") {
                unit = BRAIN.Unit.getUnit(e.data.typeID);
            } else if (e.data.type == "Bullet") {
                unit = BRAIN.Bullet.getBullet(e.data.typeID);
                var flashDirection = Math.atan2(e.data.vy, e.data.vx);
                // Create a new muzzle flash in the direction, offset by the motion of the bullet (to put it at the end of the muzzle).
                var flash = BRAIN.Particle.newMuzzleFlash(e.data.x + e.data.vx * 1.5,
                                                          e.data.y + e.data.vy * 1.5, flashDirection);
                BRAIN.particles.push(flash);
            }
			if (e.data.x != undefined) {
				unit.x = e.data.x;
			}
			if (e.data.y != undefined) {
				unit.y = e.data.y;
			}
			unit.vx = e.data.vx;
			unit.vy = e.data.vy;
			// Only update the heading if we didn't stop entirely.
			if (unit.vx != 0 || unit.vy != 0) {
				unit.direction = Math.atan2(unit.vy, unit.vx);
			}
		} else if (e.type == "ActorSeen") {
			var unit = BRAIN.Unit.newUnit(e.data.typeID, e.data.x, e.data.y, 1,
			                                 e.data.vx, e.data.vy);
			BRAIN.units.push(unit);
		} else if (e.type == "ActorHidden") {
			var unit = BRAIN.Unit.getUnit(e.data.typeID);
			unit.hidden = true;
			unit.vx = 0;
			unit.vy = 0;
		} else if (e.type == "ActorDied") {
			var unit = BRAIN.Unit.getUnit(e.data.typeID);
			unit.dead = true;
			unit.vx = 0;
			unit.vy = 0;
			BRAIN.particles.push(BRAIN.Particle.newExplosion(unit.x, unit.y));
        } else if (e.type == "WallAdded") {
            var wall = BRAIN.Wall.newWall(e.data.id, e.data.x, e.data.y, e.data.width, e.data.height);
            BRAIN.walls.push(wall);
		} else if (e.type == "TurnEnd") {
			// continue working
		} else {
            console.warn("Unknown Event encountered: " + e.type);
            console.warn(e);
        }
	};

	return {
		newEvent : newEvent,
		runEvent : runEvent,
	};
})();
