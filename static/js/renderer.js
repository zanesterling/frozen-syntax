BRAIN.setConsts({
	chasis_shape : [
			[13, -9],
			[13, -10],
			[-12, -10],
			[-12, -9],
			[-5, -6],
			[-5, 6],
			[-12, 9],
			[-12, 10],
			[13, 10],
			[13, 9],
			[11, 6],
			[11, -6]
			],
	turret_shape : [
			[0, -1],
			[-10, -1],
			[-10, 1],
			[0, 1],
			[3, 3],
			[5, 0],
			[3, -3]
			]
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

		clearScreen();
		ctx.save();
		ctx.translate(canvas.width / 2, canvas.height / 2);
		ctx.scale(zoomLevel, zoomLevel);
		ctx.translate(-zoomCenter[0], -zoomCenter[1]);
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
		ctx.strokeStyle = unit.team == 0 ?
		                "rgb(15,100,15)" : "rgb(110,15,15)";
		ctx.fillStyle = unit.team == 0 ?
		                "rgb(30,200,30)" : "rgb(220,30,30)";
		// Draw chasis
		ctx.beginPath();
		ctx.moveTo(BRAIN.chasis_shape[0][0], BRAIN.chasis_shape[0][1]);
		for (var i = 0; i < BRAIN.chasis_shape.length; i++) {
			ctx.lineTo(BRAIN.chasis_shape[i][0], BRAIN.chasis_shape[i][1]);
		}
		ctx.closePath();
		ctx.fill();
		ctx.stroke();
		
		// draw turret
		ctx.beginPath();
		ctx.moveTo(BRAIN.turret_shape[0][0], BRAIN.turret_shape[0][1]);
		for (var i = 0; i < BRAIN.turret_shape.length; i++) {
			ctx.lineTo(BRAIN.turret_shape[i][0], BRAIN.turret_shape[i][1]);
		}

		ctx.closePath();
		ctx.fill();
		ctx.stroke();

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
