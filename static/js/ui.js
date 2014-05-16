BRAIN.setConsts({
	selectedUnit : null,
	lastClick : null,
	zoomLevel : 1,
});

BRAIN.UI = (function() {

	var setup = function() {
		BRAIN.canvas.onclick = onClick;
		BRAIN.canvas.addEventListener('mousewheel', onMousewheel, false);
		BRAIN.zoomCenter = [BRAIN.canvas.width / 2, BRAIN.canvas.height / 2];
	};

	var onClick = function(event) {
		var point = {
			x : event.offsetX,
			y : event.offsetY,
		};

		if (BRAIN.selectedUnit == null) {
			for (var i = 0; i < BRAIN.units.length; i++) {
				var unit = BRAIN.units[i];
				if (pointInCircle(point, unit, 10)) {
					select(unit);
					return;
				}
			}
		} else {
			for (var i = 0; i < BRAIN.units.length; i++) {
				var unit = BRAIN.units[i];
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

	var onMousewheel = function(event) {
		if (event.wheelDelta < 0) {
			BRAIN.zoomLevel /= 1.05;
		} else {
			BRAIN.zoomLevel *= 1.05;
		}
		return false;
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
		onMousewheel : onMousewheel,
		select : select,
		toggleUI : toggleUI,
	};
})();
