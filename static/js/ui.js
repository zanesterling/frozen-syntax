BRAIN.setConsts({
	selectedUnit : null,
	lastClick : null,
	clickPoint : null,
	maxClickDist : 5,
	zoomCenter : null,
	zoomLevel : 1,
	mouseDown : false,
	mouseLoc : null,
});

BRAIN.UI = (function() {

	var setup = function() {
		BRAIN.canvas.onmousemove = onMouseMove;
		BRAIN.canvas.onmousedown = onMouseDown;
		BRAIN.canvas.onmouseup   = onMouseUp;
		BRAIN.canvas.onclick     = onClick;
		BRAIN.canvas.addEventListener('mousewheel', onMousewheel, false);
		BRAIN.zoomCenter = [BRAIN.canvas.width / 2, BRAIN.canvas.height / 2];
		document.getElementById("submit-code").onclick = submitCode;
		document.getElementById("replay").onclick = BRAIN.restart;
		BRAIN.gameId = parseInt($("#hidden-data").find(".game-id").text());
	};

	var onMouseMove = function(event) {
		mouseLoc = null;
		if (BRAIN.mouseDown) {
			if (BRAIN.mouseLoc != null) {
				BRAIN.shouldRedraw = true;
				var dx = event.x - BRAIN.mouseLoc[0];
				var dy = event.y - BRAIN.mouseLoc[1];
				BRAIN.zoomCenter[0] -= dx / BRAIN.zoomLevel;
				BRAIN.zoomCenter[1] -= dy / BRAIN.zoomLevel;
			}
			BRAIN.mouseLoc = [event.x, event.y];
		}
	};

	var onMouseDown = function(event) {
		BRAIN.mouseDown = true;
		BRAIN.clickPoint = [event.x, event.y];
	};

	var onMouseUp = function(event) {
		BRAIN.mouseDown = false;
		BRAIN.mouseLoc = null;

		var dist = Math.sqrt(Math.pow(event.x - BRAIN.clickPoint[0], 2) +
			                 Math.pow(event.y - BRAIN.clickPoint[1], 2));
		BRAIN.wasClick = dist < BRAIN.maxClickDist;
	};

	var onClick = function(event) {
		BRAIN.shouldRedraw = true;
		if (!BRAIN.wasClick) return;

		var point = {
			x : event.offsetX + BRAIN.zoomCenter[0] - BRAIN.canvas.width  / 2,
			y : event.offsetY + BRAIN.zoomCenter[1] - BRAIN.canvas.height / 2,
		};

		if (BRAIN.selectedUnit == null) {
			for (var i = 0; i < BRAIN.units.length; i++) {
				var unit = BRAIN.units[i];
				if (pointInCircle(point, unit, 10)) {
					select(unit);
					return;
				}
			}
		} else {
			for (var i = 0; i < BRAIN.units.length; i++) {
				var unit = BRAIN.units[i];
				if (pointInCircle(point, unit, 10)) {
					if (unit == BRAIN.selectedUnit) {
						deselect();
					} else {
						select(unit);
					}
					return;
				}
			}

			// no collision: deselect
			deselect();
		}
	};

	var onMousewheel = function(event) {
        event.preventDefault(); // Cancel default behavior so the user can scroll on the canvas without scrolling the page
		BRAIN.shouldRedraw = true;
		if (event.wheelDelta < 0) {
			BRAIN.zoomLevel /= 1.05;
		} else {
			BRAIN.zoomLevel *= 1.05;
		}
		return false;
	};

	var pointInCircle = function(point, circle, r) {
		var dx = circle.x - point.x;
		var dy = circle.y - point.y;
		return dx*dx + dy*dy < r*r;
	};

	var select = function(unit) {
		BRAIN.selectedUnit = unit;
	};

	var deselect = function() {
		BRAIN.selectedUnit = null;
	};

    var lastSubmittedTime = 0;

    var showSubmittingOverlay = function() {
        var overlay = document.getElementById('submit-overlay');
        overlay.style.display = "table";
        lastSubmittedTime = new Date();
        var submitPhrases = ["Submitting...", "Contributing to the HiveMind...", "Donating Efforts...", "Uploading Consiousness...",
            "Exporting Jargon...", "Sugaring Syntax...", "Reticulating Splines...", "Shifting Paradigms...", "Synergizing Outlooks...",
            "Redefining the Cloud...", "Cursing Enemies...", "Encouraging Anarchy...", "Integrating...", "Setting P = NP...",
            "Violating the Laws of Thermodynamics...", "...", "Verifying Hypothesis...", "Searching for Intelligence...",
            "Decrementing Counters...", "Looking Behind You...", "Constructing Army...", "Applying Fourier Transforms...",
            "Accelerating Moore's Law...", "Sealing Fate..."];
        var submitPhrase = submitPhrases[Math.floor(Math.random() * submitPhrases.length)];
        document.getElementById('submit-phrase').innerHTML = submitPhrase;
    };

    var hideSubmittingOverlay = function() {
        // Don't remove the overlay until it's been at least 1 second
        if (new Date() - lastSubmittedTime > 1000) {
            var overlay = document.getElementById('submit-overlay');
            overlay.style.display = "none";
        } else {
            // Schedule this function to run again in the correct amount of time
            setTimeout(hideSubmittingOverlay, new Date() - lastSubmittedTime);
        }
    };

	var submitCode = function() {
        showSubmittingOverlay();
        if (BRAIN.gameDemo) {
            $.post('/gamedemo', undefined, function(d) {
                hideSubmittingOverlay();
                BRAIN.setEventList(d);
            }, 'json');
        } else {
            $.post('/action', {
                action  : 'submit-code',
                src     : BRAIN.codeInput.getValue(),
                game_id : BRAIN.gameId,
            }, hideSubmittingOverlay);
            BRAIN.submittedCode = true;
        }
	};

	return {
		setup : setup,
		onClick : onClick,
		onMousewheel : onMousewheel,
		select : select,
	};
})();
