def match_username(form):
	results = db.matchUsername(form['username'])
	results = [account['username'] for account in results]
	if session['username'] in results:
		results.remove(session['username'])
	return json.dumps(results)

def submit_code(form):
	game = db.getGame(int(form['game_id']))
	player_id = game['players'].index(session['username'])

	# if the player hasn't already submitted src
	if int(game['turn']) > len(game['srces'][player_id]):
		# submit his src
		game['srces'][player_id].append(form['src'])
		game_data = {'srces': game['srces']}
		db.updateGame(int(form['game_id']), game_data)

	return "sonofabitch" # tryna submit mo src

def get_json(form):
	game = db.getGame(int(request.form['game_id']))
	player_id = game['players'].index(session['username'])
	return json.dumps({'jsons': game['jsons'][player_id]})
