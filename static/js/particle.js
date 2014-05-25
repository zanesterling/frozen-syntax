BRAIN.Particle = (function() {

	var setup = function() {
		Math.easeInOutQuad = function (t, b, c, d) {
			t /= d/2;
			if (t < 1) return c/2*t*t + b;
			t--;
			return -c/2 * (t*(t-2) - 1) + b;
		};
	};

	var newParticle = function(x, y, rad, isDeadFunc, renderFunc, updateFunc) {
		return {
			x : x,
			y : y,
			rad : rad,
			age : 0,
			isDeadFunc : isDeadFunc,
			renderFunc : renderFunc,
			updateFunc : updateFunc
		};
	};

	var newExplosion = function(x, y) {
		var expl = newParticle(x, y, r, isDeadExplosion,
		                           BRAIN.Renderer.renderExplosion, updateExplosion);
		expl.maxAge = 50 + Math.random() * 25;
		expl.r = 255;
		expl.g = 255;
		expl.b = 255;
	};

	var isDeadExplosion = function(expl) {
		return expl.age > expl.maxAge;
	};

	var updateExplosion = function(expl) {
		expl.rad = Math.easeInOutQuad(expl.age, 0, 20, expl.maxAge);
		expl.r = 255;
		expl.g = Math.easeInOutQuad(expl.age, 255, 0, expl.maxAge*2/3);
		expl.b = Math.easeInOutQuad(expl.age, 255, 0, expl.maxAge/2);
		expl.a = Math.easeInOutQuad(expl.age, 255, 0, expl.maxAge);
		expl.age++;
	};

	return {
		newParticle : newParticle,
	};
});
