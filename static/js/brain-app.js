var BRAIN = {
	frameLen : 1000 / 60,
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
	BRAIN.codeInput = document.getElementById("code-input");
	BRAIN.codeInput.style.width = "800px";
	BRAIN.codeInput.style.height = "200px";
	BRAIN.agents.push(BRAIN.Agent.newAgent(50, 50));
}

BRAIN.run = function() {
	BRAIN.Renderer.render();
	setTimeout
}
