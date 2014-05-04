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
		if (e.type == "actor-spawned") {
			var unit = BRAIN.Unit.newUnit(e.id, e.props.x, e.props.y);
			BRAIN.units.push(unit);
		} else if (e.type == "actor-started-moving") {
			var unit = BRAIN.Unit.getUnit(e.id);
			unit.vx = e.props.vx;
			unit.vy = e.props.vy;
			unit.direction = Math.atan2(unit.vy, unit.vx);
		} else if (e.type == "actor-stopped") {
			var unit = BRAIN.Unit.getUnit(e.id);
			unit.vx = 0;
			unit.vy = 0;
		} else if (e.type == "actor-seen") {
			var unit = BRAIN.Unit.newUnit(e.id, e.props.x, e.props.y, 1,
			                                 e.props.vx, e.props.vy);
			BRAIN.units.push(unit);
		} else if (e.type == "actor-hidden") {
			BRAIN.Unit.removeUnit(e.id);
		}
	};

	return {
		newEvent : newEvent,
		runEvent : runEvent,
	};
})();
