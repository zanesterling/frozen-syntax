BRAIN.setConsts({
});

BRAIN.Renderer = (function() {

	var setup = function() {
		BRAIN.canvas = document.getElementById("canvas"),
		BRAIN.ctx = BRAIN.canvas.getContext("2d");
	};

	var render = function() {
		clearScreen();
		for (var i = 0; i < BRAIN.units.length; i++) {
			drawUnit(BRAIN.units[i]);
		}
		drawUI();
		drawSelection();
	};

	var clearScreen = function() {
		var canvas      = BRAIN.canvas,
		    ctx         = BRAIN.ctx;

		ctx.fillStyle = "rgb(0,0,150)";
		ctx.fillRect(0, 0, canvas.width, canvas.height);
	};

	var drawUnit = function(unit) {
		var ctx = BRAIN.ctx;
		ctx.save();
		ctx.translate(unit.x, unit.y);

		// fill unit's directional stick
		var theta = unit.direction + Math.PI;
		ctx.rotate(theta);
		ctx.fillStyle = unit.team == 0 ?
		                "rgb(30,200,30)" : "rgb(220,30,30)";
		ctx.fillRect(-10, -10, 20, 20);
		ctx.fillStyle = "rgb(0,0,0)";
		ctx.fillRect(-10, -1, 10, 2);
		ctx.restore();
	};

	var drawUI = function() {
		
	};

	var drawSelection = function() {
		if (BRAIN.selectedUnit == null) {
			return;
		}

		var ctx = BRAIN.ctx;

		ctx.save();
		ctx.translate(BRAIN.selectedUnit.x, BRAIN.selectedUnit.y);
		ctx.fillStyle = "rgb(0,0,255)";
		ctx.fillRect(-5, -5, 10, 10);
		ctx.restore();
	};

	return {
		setup : setup,
		render : render,
	};
})();
