BRAIN.setConsts({
	borderWidth : 3,
});

BRAIN.Renderer = (function() {

	var setup = function() {
		BRAIN.canvas = document.getElementById("canvas"),
		BRAIN.ctx = BRAIN.canvas.getContext("2d");
	};

	var render = function() {
		clearScreen();
		drawBorder();
		for (var i = 0; i < BRAIN.agents.length; i++) {
			drawAgent(BRAIN.agents[i]);
		}
	};

	var clearScreen = function() {
		var canvas      = BRAIN.canvas,
		    ctx         = BRAIN.ctx,
		    borderWidth = BRAIN.borderWidth;

		ctx.fillStyle = "rgb(0,0,150)";
		ctx.fillRect(borderWidth, borderWidth,
		             canvas.width-borderWidth*2,
		             canvas.height-borderWidth*2);
	};

	var drawBorder = function() {
		var canvas      = BRAIN.canvas,
		    ctx         = BRAIN.ctx,
		    borderWidth = BRAIN.borderWidth;

		ctx.fillStyle = "rgb(0,0,10)";
		ctx.fillRect(0, 0, canvas.width-1, borderWidth);
		ctx.fillRect(0, 0, borderWidth, canvas.height-1);
		ctx.fillRect(canvas.width-borderWidth, 0,
		             borderWidth, canvas.height);
		ctx.fillRect(0, canvas.height-borderWidth,
		             canvas.width-borderWidth, borderWidth);
	};

	var drawAgent = function(agent) {
		var ctx = BRAIN.ctx;
		ctx.save();
		ctx.translate(agent.x, agent.y);

		// fill agent's directional stick
		var theta = agent.direction + Math.PI;
		ctx.rotate(theta);
		ctx.fillStyle = agent.team == 0 ?
		                "rgb(30,200,30)" : "rgb(220,30,30)";
		ctx.fillRect(-10, -10, 20, 20);
		ctx.fillStyle = "rgb(0,0,0)";
		ctx.fillRect(-10, -1, 10, 2);
		ctx.restore();
	};

	return {
		setup : setup,
		render : render,
		clearScreen : clearScreen,
		drawBorder : drawBorder,
		drawAgent : drawAgent,
	};
})();
