BRAIN.Renderer = (function() {
	var setup = function() {
		BRAIN.canvas = document.getElementById("canvas"),
		BRAIN.ctx = BRAIN.canvas.getContext("2d");
	}

	return {
		setup : setup,
	}
})();
