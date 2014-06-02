from cPickle import dumps, loads
from world import World
from flask import session
import interface
import json
import db

def match_username(form):
	results = db.matchUsername(form['username'])
	results = [account['username'] for account in results]
	if session['username'] in results:
		results.remove(session['username'])
	return json.dumps(results)

def submit_code(form):
	game = db.getGame(int(form['game_id']))
	# TODO make sure the player is in the game
	player_id = game['players'].index(session['username'])

	# if the player has already submitted src
	if int(game['turn']) <= len(game['srces'][player_id]):
		return "sonofabitch"

	# submit his src
	game['srces'][player_id].append(form['src'])

	all_submitted = all_same(map(len, game['srces']))
	if all_submitted:
		simulate_turn(game)
	store(game)
	return "all good"

def simulate_turn(game):
	# get the pickled game object
	if len(game['states']) > 0:
		world = loads(game['states'][-1].encode('ascii', 'replace'))
		world.clear_events()
	else:
		world = World(100, 100)
		world.add_unit(0, 0, 0, 10)
		world.units[0].speed = 1

	# get all srces from this turn
	last_srces = [l[-1] for l in game['srces']]

	# interpret the srces
	interface.interpret(last_srces, 250, 5, world.step, world.callbacks())

	# make sure the world ran for the whole turn
	while world.timestamp % 250 != 0:
		world.step()

	# repickle the world and store it as the newest state
	game['states'].append(dumps(world))
	for l in game['jsons']:
		l.append(world.serialized_events()) # TODO make these user-dependent

	# increment the turncount
	game['turn'] += 1

def store(game):
	db.updateGame(game['game_id'], game)

def get_json(form):
	game = db.getGame(int(form['game_id']))

	# if they're requesting a non-existent turn
	if int(game['turn']) < int(form['turn']):
		return "{'success': false}"

	# get the player's part
	player_id = game['players'].index(session['username'])
	events_list = game['jsons'][player_id]

	json_objs = events_list[:int(form['turn'])]
	objs = {'jsons': map(json.loads, json_objs)}
	objs['success'] = True;
	return json.dumps(objs)

def get_turn(form):
	game = db.getGame(int(form['game_id']))
	return str(game['turn'])

def all_same(l):
	def ats(l, v):
		return len(l) == 0 or (v == l[0] and ats(l[1:], v))
	return ats(l[1:], l[0])
