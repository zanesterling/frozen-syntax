BRAIN.setConsts({
});

BRAIN.Renderer = (function() {

	var setup = function() {
		BRAIN.canvas = document.getElementById("canvas"),
		BRAIN.ctx = BRAIN.canvas.getContext("2d");
	};

	var render = function() {
		var zoomCenter = BRAIN.zoomCenter,
		    zoomLevel = BRAIN.zoomLevel,
		    ctx = BRAIN.canvas.getContext("2d");

		ctx.save();
		ctx.translate(zoomCenter[0], zoomCenter[1]);
		ctx.scale(zoomLevel, zoomLevel);
		ctx.translate(-zoomCenter[0], -zoomCenter[1]);
		clearScreen();
		drawSelection();
		for (var i = 0; i < BRAIN.units.length; i++) {
			drawUnit(BRAIN.units[i]);
		}
		ctx.restore();
	};

	var clearScreen = function() {
		var canvas      = BRAIN.canvas,
		    ctx         = BRAIN.ctx;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
	};

	var drawUnit = function(unit) {
		var ctx = BRAIN.ctx;
		//ctx.save();
		ctx.translate(unit.x, unit.y);

		// fill unit's directional stick
		var theta = unit.direction + Math.PI;
		ctx.rotate(theta);
		ctx.fillStyle = unit.team == 0 ?
		                "rgb(30,200,30)" : "rgb(220,30,30)";
		ctx.fillRect(-10, -10, 20, 20);
		ctx.fillStyle = "rgb(0,0,0)";
		ctx.fillRect(-10, -1, 10, 2);
		ctx.rotate(-theta);
		ctx.translate(-unit.x, -unit.y);
		//ctx.restore();
	};

	var drawSelection = function() {
		if (BRAIN.selectedUnit == null) {
			return;
		}

		var ctx = BRAIN.ctx,
		    unit = BRAIN.selectedUnit;

		ctx.save();
		ctx.translate(BRAIN.selectedUnit.x, BRAIN.selectedUnit.y);
		var grd = ctx.createRadialGradient(0, 0, 0, 0, 0, 20);
		grd.addColorStop(0, unit.team == 0 ? "rgba(30,200,30,255)"
		                                   : "rgba(220,30,30,255)");
		grd.addColorStop(1, unit.team == 0 ? "rgba(30,200,30,0)"
		                                   : "rgba(220,30,30,0)");
		ctx.fillStyle = grd;
		ctx.fillRect(-20, -20, 40, 40);
		ctx.restore();
	};

	return {
		setup : setup,
		render : render,
	};
})();
