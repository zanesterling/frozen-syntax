var BRAIN = {
	frameLen : 1000 / 40,
	tickCount : 0,
	turn : 1,
	units : [],
	obstacles : [],
	particles : [],
	submittedCode : false,
	lastPing : 0,
}

window.onload = function() {
	$.getJSON("/events", function (data) {
		BRAIN.eventList = data.events;
		BRAIN.setup();
		BRAIN.Renderer.setup();
		BRAIN.UI.setup();
		BRAIN.Particle.setup();
		BRAIN.run();
		BRAIN.getTurn();
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
	BRAIN.shouldRedraw = false;
	BRAIN.events = {};
	// load and style codeInput textarea
	BRAIN.codeInput = ace.edit("codeInput");
	var LispMode = require("ace/mode/lisp").Mode;
	BRAIN.codeInput.getSession().setMode(new LispMode());
	BRAIN.codeInput.focus();
}

BRAIN.setEventList = function(newEvents) {
	BRAIN.events = {};
	for (var i = 0; i < newEvents.length; i++) {
		if (!BRAIN.events[newEvents[i].timestamp]) {
			BRAIN.events[newEvents[i].timestamp] = [];
		}
		BRAIN.events[newEvents[i].timestamp].push(newEvents[i]);
	}
	BRAIN.tickCount = 0;
	BRAIN.units = [];
	BRAIN.particles = [];
}

BRAIN.run = function() {
	var startTime = new Date().getMilliseconds(),
	    eventList = BRAIN.eventList,
	    particles = BRAIN.particles,
	    units     = BRAIN.units,
	    simulatedTick = false;

	if (BRAIN.submittedCode && (new Date()).getTime() - BRAIN.lastPing > 5000) {
		BRAIN.lastPing = (new Date()).getTime();
		BRAIN.getEvents();
	}

	// logic
	if (BRAIN.events[BRAIN.tickCount]) {
		for (var i = 0; i < BRAIN.events[BRAIN.tickCount].length; i++) {
			BRAIN.Event.runEvent(BRAIN.events[BRAIN.tickCount][i]);
			BRAIN.shouldRedraw = true;
			simulatedTick = true;
		}
	}
	if (simulatedTick) {
		//console.log("done simulating events for tick " + BRAIN.tickCount);
		BRAIN.tickCount++;

		for (var i = 0; i < units.length; i++) {
			units[i].x += units[i].vx;
			units[i].y += units[i].vy;
		}
		for (var i = 0; i < particles.length; i++) {
			particles[i].updateParticle(particles[i]);
			if (particles[i].isDead(particles[i])) {
				particles.splice(i--, 1);
			}
		}
	}

	// render
	// Get the highest timestamp that has events
	var x; for (var i in BRAIN.events) { x = i; }; x = parseInt(x);
	BRAIN.shouldRedraw |= BRAIN.tickCount < x; // If we haven't hit the end of our events, we should redraw (to render action in between actual events)
	if (BRAIN.shouldRedraw) {
		BRAIN.Renderer.render();
		//console.log("redrawing");
	}
	BRAIN.shouldRedraw = false;

	var endTime = new Date().getMilliseconds();
	var frameLen = endTime - startTime;
	document.getElementById("fps-counter").innerText = frameLen + " millis";
	setTimeout(BRAIN.run, BRAIN.framelen - frameLen);
}

BRAIN.unitGraphicsDemo = function() {
	for (var i = 0; i < 100; i++) {
		for (var j = 0; j < 10; j++) {
			BRAIN.units.push(BRAIN.Unit.newUnit(1, i * 30, j * 30));
		}
	}
	BRAIN.shouldRedraw = true;
}

BRAIN.getEvents = function() {
	$.post('/action', {
		action : 'get-json',
		game_id : BRAIN.gameId,
		turn : BRAIN.turn
	}, function(data) {
		BRAIN.submittedCode = !data.success;
		var eventsList = [];
		for (var i = 0; i < data['jsons'].length; i++) {
			for (var j = 0; j < data['jsons'][i].length; j++) {
				eventsList.push(data['jsons'][i][j]);
			}
		}
		BRAIN.setEventList(eventsList);
	}, 'json');
};

BRAIN.getTurn = function() {
	$.post('/action', {
		action : 'get-turn',
		game_id : BRAIN.gameId
	}, function(data) {
		BRAIN.turn = parseInt(data);
	}, 'json');
};

BRAIN.getState = function(turn) {
	$.post('/action', {
		action : 'get-state',
		game_id : BRAIN.gameId,
		turn : turn
	}, function(data) {

	});
};
