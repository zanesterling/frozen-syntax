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
			isDead: isDeadFunc,
			renderParticle : renderFunc,
			updateParticle : updateFunc,
		};
	};

	var newExplosion = function(x, y) {
		var expl = newParticle(x, y, 0, isDeadExplosion,
								   BRAIN.Renderer.renderExplosion, updateExplosion);
		expl.maxAge = 30 + Math.random() * 25;
		expl.r = 150;
		expl.g = 255;
		expl.b = 255;
		return expl;
	};

	var isDeadExplosion = function(expl) {
		return expl.age > expl.maxAge;
	};

	var updateExplosion = function(expl) {
		expl.rad = Math.easeInOutQuad(expl.age, 0, 30, expl.maxAge);
		expl.r = 200;
		expl.g = expl.age > expl.maxAge*2/3 ? 55 :
				 255 - Math.easeInOutQuad(expl.age, 0, 200, expl.maxAge*2/3);
		expl.b = expl.age > expl.maxAge/3 ? 0 :
				 255 - Math.easeInOutQuad(expl.age, 0, 255, expl.maxAge/3);
		expl.a = 255 - Math.easeInOutQuad(expl.age, 0, 255, expl.maxAge);
		expl.age++;
	};

	var newBulletSmoke = function(x, y) {
		return newExplosion(x, y, 2, isDeadBulletSmoke,
							BRAIN.Renderer.renderBulletSmoke, updateBulletSmoke);
	};

	var isDeadBulletSmoke = function(smoke) {
		return smoke.age > 30;
	};

	var updateBulletSmoke = function(smoke) {
		var theta = Math.random() * Math.PI * 2;
		BRAIN.ctx.fillStyle = "rgba(100, 100, 100, .5)";
		BRAIN.ctx.translate(smoke.x, smoke.y);
		BRAIN.ctx.rotate(theta);
		BRAIN.ctx.fillRect(-smoke.rad * smoke.age/30, -smoke.rad * smoke.age/30,
		smoke.rad * 2 * smoke.age/30, smoke.rad*2 * smoke.age/30);
		BRAIN.ctx.rotate(-theta);
		BRAIN.ctx.translate(-smoke.x, -smoke.y);
	};

	return {
		setup : setup,
		newParticle : newParticle,
		newExplosion : newExplosion,
		newBulletSmoke : newBulletSmoke,
	};
})();
