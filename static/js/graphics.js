window.onload = function() {
	BRAIN.canvas = document.getElementById("canvas"),
	BRAIN.ctx = BRAIN.canvas.getContext("2d");

	var canvas = BRAIN.canvas,
		ctx = BRAIN.ctx;
	
	ctx.fillStyle = "rgb(255,0,0)";
	ctx.fillRect(0, 0, canvas.width-1, 1);
	ctx.fillRect(0, 0, 1, canvas.height-1);
	ctx.fillRect(canvas.width-1, 0, 1, canvas.height);
	ctx.fillRect(0, canvas.height-1, canvas.width-1, 1);
	ctx.clearRect(1, 1, canvas.width-2, canvas.height-2);
};

var BRAIN = {
}
