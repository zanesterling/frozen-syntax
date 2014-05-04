var BRAIN = {
	frameLen : 1000 / 40,
	tickCount : 0,
	agents : [],
	obstacles : [],
}

window.onload = function() {
	$.getJSON("http://" + window.location.host + "/events", function (data) {
		BRAIN.eventList = data.events;
		BRAIN.setup();
		BRAIN.Renderer.setup();
		BRAIN.UI.setup();
		BRAIN.run();
	});
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

	$('#toggleButton').click(BRAIN.UI.toggleUI);
}

BRAIN.run = function() {
	var startTime = new Date().getMilliseconds(),
		eventList = BRAIN.eventList,
		agents    = BRAIN.agents;

	// logic
	for (var i = 0; i < eventList.length; i++) {
		if (eventList[i].timestamp == BRAIN.tickCount) {
			BRAIN.Event.runEvent(eventList[i]);
		}
	}
	BRAIN.tickCount++;

	for (var i = 0; i < agents.length; i++) {
		agents[i].x += agents[i].vx;
		agents[i].y += agents[i].vy;
	}

	// render
	BRAIN.Renderer.render();

	var endTime = new Date().getMilliseconds();
	var frameLen = endTime - startTime;
	document.getElementById("fps-counter").innerText = frameLen +
	                                                   " millis";
	setTimeout(BRAIN.run, BRAIN.framelen - frameLen);
}

BRAIN.agentGraphicsDemo = function() {
	var floor = Math.floor;
	for (var i = 0; i < 165; i++) {
		BRAIN.agents.push(BRAIN.Agent.newAgent(50*(1+i%15),
		                                       50*(floor(1+i/15)), i%2));
	}
}
