import jcli
import db

def match_username(form):
	results = db.matchUsername(form['username'])
	results = [account['username'] for account in results]
	if session['username'] in results:
		results.remove(session['username'])
	return json.dumps(results)

def submit_code(form):
	game = db.getGame(int(form['game_id']))
	player_id = game['players'].index(session['username'])

	# if the player has already submitted src
	if int(game['turn']) <= len(game['srces'][player_id]):
		return "sonofabitch"

	# submit his src
	game['srces'][player_id].append(form['src'])
	game_data = {'srces': game['srces']}

	all_submitted = all_same(map(len, game['srces']))
	if all_submitted:
		simulate(game)
	store(game)

def simulate(game): # TODO
	game['turn'] += 1

def store(game):
	db.updateGame(game['id'], game)

def get_json(form):
	game = db.getGame(int(request.form['game_id']))
	player_id = game['players'].index(session['username'])
	return json.dumps({'jsons': game['jsons'][player_id]})

def all_same(l):
	def ats(l, v):
		return v == l[0] and ats(l[1:], v)
	return ats(l[1:], l[0])
