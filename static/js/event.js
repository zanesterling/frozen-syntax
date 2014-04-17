BRAIN.Event = (function() {
	var newEvent = function(type, id, timestamp, props) {
		return {
			type : type,
			id : id,
			timestamp : timestamp,
			props : props
		};
	};

	var runEvent = function(e) {
		if (e.type == "actor-spawned") {
			var agent = BRAIN.Agent.newAgent(e.id, e.props.x, e.props.y);
			BRAIN.agents.push(agent);
		} else if (e.type == "actor-started-moving") {
			var agent = BRAIN.Agent.getAgent(e.id);
			agent.vx = e.props.vx;
			agent.vy = e.props.vy;
			agent.direction = Math.atan2(agent.vy, agent.vx);
		} else if (e.type == "actor-stopped") {
			var agent = BRAIN.Agent.getAgent(e.id);
			agent.vx = 0;
			agent.vy = 0;
		} else if (e.type == "actor-seen") {
			var agent = BRAIN.Agent.newAgent(e.id, e.props.x, e.props.y, 1,
			                                 e.props.vx, e.props.vy);
			BRAIN.agents.push(agent);
		} else if (e.type == "actor-hidden") {
			BRAIN.Agent.removeAgent(e.id);
		}
	};

	return {
		newEvent : newEvent,
		runEvent : runEvent,
	};
})();
