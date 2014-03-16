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

		ctx.clearRect(borderWidth, borderWidth,
		              canvas.width-borderWidth*2-1, canvas.height-borderWidth*2-1);
	};

	var drawBorder = function() {
		var canvas      = BRAIN.canvas,
		    ctx         = BRAIN.ctx,
		    borderWidth = BRAIN.borderWidth;

		ctx.fillStyle = "rgb(255,0,0)";
		ctx.fillRect(0, 0, canvas.width-1, borderWidth);
		ctx.fillRect(0, 0, borderWidth, canvas.height-1);
		ctx.fillRect(canvas.width-borderWidth, 0, borderWidth, canvas.height);
		ctx.fillRect(0, canvas.height-borderWidth,
		             canvas.width-borderWidth, borderWidth);
	};

	var drawAgent = function(agent) {
		var ctx = BRAIN.ctx;

		ctx.fillStyle = "rgb(0,0,255)";
		ctx.arc(agent.x, agent.y, 10, 0, Math.PI*2);
		ctx.fill();
	};

	return {
		setup : setup,
		render : render,
		clearScreen : clearScreen,
		drawBorder : drawBorder,
		drawAgent : drawAgent,
	};
})();
