BRAIN.setConsts({
	selectedUnit : null,
	lastClick : null,
	clickPoint : null,
	maxClickDist : 5,
	zoomCenter : null,
	zoomLevel : 1,
	mouseDown : false,
	mouseLoc : null,
});

BRAIN.UI = (function() {

	var setup = function() {
		BRAIN.canvas.onmousemove = onMouseMove;
		BRAIN.canvas.onmousedown = onMouseDown;
		BRAIN.canvas.onmouseup   = onMouseUp;
		BRAIN.canvas.onclick     = onClick;
		BRAIN.canvas.addEventListener('mousewheel', onMousewheel, false);
		BRAIN.zoomCenter = [BRAIN.canvas.width / 2, BRAIN.canvas.height / 2];
		document.getElementById("submit-code").onclick = submitCode;
		BRAIN.gameId = parseInt($("#hidden-data").find(".game-id").text());
	};

	var onMouseMove = function(event) {
		mouseLoc = null;
		if (BRAIN.mouseDown) {
			if (BRAIN.mouseLoc != null) {
				var dx = event.x - BRAIN.mouseLoc[0];
				var dy = event.y - BRAIN.mouseLoc[1];
				BRAIN.zoomCenter[0] -= dx / BRAIN.zoomLevel;
				BRAIN.zoomCenter[1] -= dy / BRAIN.zoomLevel;
			}
			BRAIN.mouseLoc = [event.x, event.y];
		}
	};

	var onMouseDown = function(event) {
		BRAIN.mouseDown = true;
		BRAIN.clickPoint = [event.x, event.y];
	};

	var onMouseUp = function(event) {
		BRAIN.mouseDown = false;
		BRAIN.mouseLoc = null;

		var dist = Math.sqrt(Math.pow(event.x - BRAIN.clickPoint[0], 2) +
			                 Math.pow(event.y - BRAIN.clickPoint[1], 2));
		BRAIN.wasClick = dist < BRAIN.maxClickDist;
	};

	var onClick = function(event) {
		if (!BRAIN.wasClick) return;

		var point = {
			x : event.offsetX + BRAIN.zoomCenter[0] - BRAIN.canvas.width  / 2,
			y : event.offsetY + BRAIN.zoomCenter[1] - BRAIN.canvas.height / 2,
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

	var submitCode = function() {
		//$.post('/action', {
			//action : 'submit-code',
			//src    : BRAIN.codeInput.getValue(),
			//game_id : BRAIN.gameId,
		//});
		$.post('/gamedemo', {}, function(data) {
			BRAIN.eventList = data;
			BRAIN.tickCount = 0;
		}, "json");
	};

	return {
		setup : setup,
		onClick : onClick,
		onMousewheel : onMousewheel,
		select : select,
		toggleUI : toggleUI,
	};
})();
