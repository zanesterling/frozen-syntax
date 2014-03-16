BRAIN.Agent = (function() {
	var newAgent = function(x, y) {
		return {
			x : x,
			y : y,
		};
	};

	return {
		newAgent : newAgent,
	};
})();
