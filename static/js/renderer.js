BRAIN.setConsts({
	chasis_shape : [
			[10, -9],
			[10, -10],
			[-15, -10],
			[-15, -9],
			[-8, -6],
			[-8, 6],
			[-15, 9],
			[-15, 10],
			[10, 10],
			[10, 9],
			[8, 6],
			[8, -6]
			],
	turret_shape : [
			[-3, -1],
			[-13, -1],
			[-13, 1],
			[-3, 1],
			[0, 3],
			[2, 0],
			[0, -3],
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
		for (var i = 0; i < BRAIN.particles.length; i++) {
			BRAIN.particles[i].renderParticle(BRAIN.particles[i]);
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
		ctx.translate(unit.x, unit.y);

		// fill unit's directional stick
		var theta = unit.direction + Math.PI;
		ctx.rotate(theta);

		var teamColor = unit.team == 0 ?
		                "rgb(30,200,30)" : "rgb(220,30,30)";
		var strokeColor = unit.team == 0 ?
		                "rgb(15,100,15)" : "rgb(110,15,15)";

		if (unit.dead) {
			teamColor = unit.team == 0 ? "rgb(10,60,10)" : "rgb(65,10,10)";
			strokeColor = "rgb(0,0,0)";
		} else if (unit.hidden) {
			//teamColor = unit.team == 0 ?
					//"rgba(30, 60, 30, 1)" : "rgba(60, 30, 30, 1)";
			var buff = teamColor;
			teamColor = strokeColor;
			strokeColor = buff;
		}

		ctx.strokeStyle = strokeColor;

		drawChassis(teamColor, theta);
		drawTurret(teamColor, theta);

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

	var renderExplosion = function(expl) {
		var ctx = BRAIN.ctx;
		var r = Math.floor(expl.r);
		var g = Math.floor(expl.g);
		var b = Math.floor(expl.b);
		var a = Math.floor(expl.a);
		ctx.translate(expl.x, expl.y);

		var grd = ctx.createRadialGradient(0, 0, 0, 0, 0, expl.rad);
		grd.addColorStop(0, "rgba(" + r + "," + g + "," + b + "," + a + ")");
		grd.addColorStop(1, "rgba(" + r + "," + g + "," + b + ",0)");
		ctx.fillStyle = grd;
		ctx.fillRect(-expl.rad, -expl.rad, expl.rad*2, expl.rad*2);

		ctx.translate(-expl.x, -expl.y);
	};

	var drawChassis = function(teamColor, theta) {
		var shadowColor = "rgba(0, 0, 0, .2)";
		var shadowTheta = theta + Math.PI/4;
		var shadowx = -3 * Math.cos(shadowTheta);
		var shadowy = 3 * Math.sin(shadowTheta);
		var ctx = BRAIN.ctx;

		// Draw chassis shadow
		ctx.fillStyle = shadowColor;
		ctx.beginPath();
		ctx.moveTo(BRAIN.chasis_shape[0][0] * 1.1 + shadowx,
		           BRAIN.chasis_shape[0][1] * 1.1 + shadowy);
		for (var i = 0; i < BRAIN.chasis_shape.length; i++) {
			ctx.lineTo(BRAIN.chasis_shape[i][0] * 1.1 + shadowx,
			           BRAIN.chasis_shape[i][1] * 1.1 + shadowy);
		}
		ctx.closePath();
		ctx.fill();

		ctx.fillStyle = teamColor;

		// Draw chasis
		ctx.beginPath();
		ctx.moveTo(BRAIN.chasis_shape[0][0],
		           BRAIN.chasis_shape[0][1]);
		for (var i = 0; i < BRAIN.chasis_shape.length; i++) {
			ctx.lineTo(BRAIN.chasis_shape[i][0],
			           BRAIN.chasis_shape[i][1]);
		}
		ctx.closePath();
		ctx.fill();
		ctx.stroke();
	};

	var drawTurret = function(teamColor, theta) {
		var shadowColor = "rgba(0, 0, 0, .2)";
		var shadowTheta = theta + Math.PI/4;
		var shadowx = -1 * Math.cos(shadowTheta);
		var shadowy = 1 * Math.sin(shadowTheta);
		var ctx = BRAIN.ctx;

		// Draw turret shadow
		ctx.fillStyle = shadowColor;
		ctx.beginPath();
		ctx.moveTo(BRAIN.turret_shape[0][0] * 1.1 + shadowx,
		           BRAIN.turret_shape[0][1] * 1.1 + shadowy);
		for (var i = 0; i < BRAIN.turret_shape.length; i++) {
			ctx.lineTo(BRAIN.turret_shape[i][0] * 1.1 + shadowx,
			           BRAIN.turret_shape[i][1] * 1.1 + shadowy);
		}
		ctx.closePath();
		ctx.fill();

		// Draw turret
		ctx.fillStyle = teamColor;
		ctx.beginPath();
		ctx.moveTo(BRAIN.turret_shape[0][0],
		           BRAIN.turret_shape[0][1]);
		for (var i = 0; i < BRAIN.turret_shape.length; i++) {
			ctx.lineTo(BRAIN.turret_shape[i][0],
			           BRAIN.turret_shape[i][1]);
		}

		ctx.closePath();
		ctx.fill();
		ctx.stroke();
	}

	return {
		setup : setup,
		render : render,
		renderExplosion : renderExplosion,
	};
})();
