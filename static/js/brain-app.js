var BRAIN = {
	frameLen : 1000 / 40,
	tickCount : 0,
	units : [],
    bullets : [],
    walls : [],
	obstacles : [],
	particles : [],
}

window.onload = function() {
	$.getJSON("http://" + window.location.host + "/events", function (data) {
		BRAIN.eventList = data.events;
		BRAIN.setup();
		BRAIN.Renderer.setup();
		BRAIN.UI.setup();
		BRAIN.Particle.setup();
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
		if (newEvents[i].length) {
		    BRAIN.events[i] = newEvents[i]
		}
	}
	BRAIN.tickCount = 0;
	BRAIN.units = [];
    BRAIN.bullets = [];
    BRAIN.walls = [];
	BRAIN.particles = [];
}

BRAIN.run = function() {
	var startTime = new Date().getMilliseconds(),
	    eventList = BRAIN.eventList,
	    particles = BRAIN.particles,
	    units     = BRAIN.units,
	    bullets   = BRAIN.bullets,
	    simulatedTick = false;

	// Get the highest timestamp that has events
    var moreEvents = false
	var x; for (var i in BRAIN.events) { x = i; }; x = parseInt(x);
	moreEvents |= BRAIN.tickCount < x;

	// logic
	if (BRAIN.events[BRAIN.tickCount]) {
		for (var i = 0; i < BRAIN.events[BRAIN.tickCount].length; i++) {
			BRAIN.Event.runEvent(BRAIN.events[BRAIN.tickCount][i]);
			BRAIN.shouldRedraw = true;
			simulatedTick = true;
		}
	}
    if (simulatedTick || moreEvents) {
		//console.log("done simulating events for tick " + BRAIN.tickCount);
		BRAIN.tickCount++;

		for (var i = 0; i < units.length; i++) {
			units[i].x += units[i].vx;
			units[i].y += units[i].vy;
		}
        for (var i = 0; i < bullets.length; i++) {
            console.log("Moving bullet");
            bullets[i].x += bullets[i].vx;
            bullets[i].y += bullets[i].vy;
        }
		for (var i = 0; i < particles.length; i++) {
			particles[i].updateParticle(particles[i]);
			if (particles[i].isDead(particles[i])) {
				particles.splice(i--, 1);
			}
		}
    }

	// render
    BRAIN.shouldRedraw |= moreEvents; // If there are more events, we should render
	if (BRAIN.shouldRedraw) {
		BRAIN.Renderer.render();
		//console.log("redrawing");
	}
	BRAIN.shouldRedraw = false;

	var endTime = new Date().getMilliseconds();
	var frameLen = endTime - startTime;
	document.getElementById("fps-counter").innerText = frameLen +
	                                                   " millis";
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
