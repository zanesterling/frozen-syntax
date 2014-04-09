var BRAIN = {
	frameLen : 1000 / 40,
	agents : [],
}

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
	// load and style codeInput textarea
	BRAIN.codeInput = ace.edit("codeInput");
	var LispMode = require("ace/mode/lisp").Mode;
	BRAIN.codeInput.getSession().setMode(new LispMode());
	BRAIN.codeInput.focus();

	var floor = Math.floor;
	for (var i = 0; i < 165; i++) {
		BRAIN.agents.push(BRAIN.Agent.newAgent(50*(1+i%15), 50*(floor(1+i/15)), i%2));
	}
}

BRAIN.run = function() {
	var startTime = new Date().getMilliseconds();

	// logic
	for (var i = 0; i < BRAIN.agents.length; i++) {
		BRAIN.agents[i].direction = (BRAIN.agents[i].direction + 0.01) % (Math.PI*2);
	}

	// render
	BRAIN.Renderer.render();

	var endTime = new Date().getMilliseconds();
	var frameLen = endTime - startTime;
	document.getElementById("fps-counter").innerText = frameLen + " millis";
	setTimeout(BRAIN.run, BRAIN.framelen - frameLen);
}
