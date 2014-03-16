var BRAIN = {}

window.onload = function() {
	BRAIN.setup();
	BRAIN.Renderer.setup();
	BRAIN.run();
};

// With thanks to Wolfenstein3D-browser
BRAIN.setConsts = function(C) {
    for (var a in C) {
        if (C.hasOwnProperty(a) && !(a in BRAIN)) {
            BRAIN[a] = C[a];
        }
    }
}

//If v is undefined, return d, else return v
BRAIN.defaultTo = function(v, d) {
    return typeof v != "undefined" ? v : d;
}

BRAIN.setup = function() {
}

BRAIN.run = function() {
	var canvas = BRAIN.canvas,
		ctx = BRAIN.ctx;
	
	ctx.fillStyle = "rgb(255,0,0)";
	ctx.fillRect(0, 0, canvas.width-1, 1);
	ctx.fillRect(0, 0, 1, canvas.height-1);
	ctx.fillRect(canvas.width-1, 0, 1, canvas.height);
	ctx.fillRect(0, canvas.height-1, canvas.width-1, 1);
	ctx.clearRect(1, 1, canvas.width-2, canvas.height-2);
}
