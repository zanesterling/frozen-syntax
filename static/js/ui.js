BRAIN.setConsts({
	selectedUnit : null,
	lastClick : null,
});

BRAIN.UI = (function() {

	var setup = function() {
		BRAIN.canvas.onclick = onClick;
	};

	var onClick = function(event) {
		var point = {
			x : event.offsetX,
			y : event.offsetY,
		};

		if (BRAIN.selectedUnit == null) {
			for (var i = 0; i < BRAIN.agents.length; i++) {
				var unit = BRAIN.agents[i];
				if (pointInCircle(point, unit, 10)) {
					select(unit);
					return;
				}
			}
		} else {
			for (var i = 0; i < BRAIN.agents.length; i++) {
				var unit = BRAIN.agents[i];
				if (pointInCircle(point, unit, 10)) {
					if (unit == BRAIN.selectedUnit) {
						deselect();
					} else {
						select(unit);
					}
					return;
				}
			}

			// no collision: deselect
			deselect();
		}
	};

	var pointInCircle = function(point, circle, r) {
		var dx = circle.x - point.x;
		var dy = circle.y - point.y;
		return dx*dx + dy*dy < r*r;
	};

	var select = function(unit) {
		BRAIN.selectedUnit = unit;
	};

	var deselect = function() {
		BRAIN.selectedUnit = null;
	};

	var toggleUI = function() {
		$('#ui').slideToggle();
		$('#codeInput').slideToggle();
	};

	return {
		setup : setup,
		onClick : onClick,
		select : select,
		toggleUI : toggleUI,
	};
})();
