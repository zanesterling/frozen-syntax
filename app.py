from flask import Flask, render_template, session, request, redirect, url_for, flash
import json
import md5
import error
import db
import world
import world2
import unit
import random

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/')
def home():
	d = {'logged_in': 'username' in session}
	return render_template("home.html", d=d)

@app.route('/register', methods=["GET","POST"])
def register():
	# eject users who are logged in
	if 'username' in session:
		return redirect(url_for('home'))

	d = {"errors": []}
	d['logged_in'] = 'username' in session
	if request.method == "GET":
		return render_template("register.html", d=d)
	
	# POST
	errors = db.create_account(request.form)
	if errors:
		d['errors'] = errors
		for e in errors:
			flash(error.userify(e), "error")
		return render_template("register.html", d=d)

	# no errors
	session['username'] = request.form['username']
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect(url_for('home'))

@app.route('/login', methods=["GET", "POST"])
def login():
	if 'username' in session:
		return redirect(url_for('home'))

	d = {'errors': []}
	d['logged_in'] = False
	if request.method == 'GET':
		return render_template('login.html', d=d)
	
	# POST
	if db.login(request.form):
		session['username'] = request.form['username']
		return redirect(url_for('home'))

	# oh noes, errors
	d['errors'] = ['login-fail']
	flash(error.userify('login-fail'), "error")
	return render_template("login.html", d=d)

@app.route('/user/<username>')
def user(username):
	d = {}
	d['logged_in'] = 'username' in session
	d['user_info'] = db.getInfo(username)
	games = db.getActiveGames()
	gameslist = []
	for game in games:
		if username in game['players']:
			game['players'] = [db.getInfo(user) for user in game['players']]
			gameslist.append(game)
	d['games'] = gameslist
	return render_template('account.html', d=d)

@app.route('/play/')
def play():
	d = {'logged_in': 'username' in session}
	return render_template("play.html", d=d)

@app.route('/play/solo/')
def solo():
	d = {'logged_in': 'username' in session}
	return render_template("solo.html", d=d)

@app.route('/play/versus/')
def versus():
	d = {'logged_in': 'username' in session}
	games = db.getActiveGames()
	for game in games:
		game['players'] = [db.getInfo(username) for username in game['players']]
	d['games'] = games
	return render_template("versus.html", d=d)

@app.route('/play/versus/create', methods=["GET", "POST"])
def versusCreate():
	d = {'logged_in': 'username' in session}
	if request.method == "GET":
		d['user'] = db.getInfo(session['username'])
		return render_template("versus-create.html", d=d)
	
	#POST
	db.newGame(request.form)
	return redirect(url_for('versus'))

@app.route('/play/<int:game_id>')
def playGame(game_id):
	d = {'logged_in': 'username' in session}
	if not d['logged_in']:
		return redirect(url_for('home'))

	d['game'] = db.getGame(game_id)
	d['players'] = [db.getInfo(usern) for usern in d['game']['players']]
	d['user'] = db.getInfo(session['username'])
	return render_template('play-game.html', d=d)

@app.route('/learn/')
def learn():
	d = {'logged_in': 'username' in session}
	return render_template("learn.html", d=d)

@app.route('/action', methods=["POST"])
def action():
	# return all usernames matching the given regex
	if request.form['action'] == 'match-username':
		results = db.matchUsername(request.form['username'])
		results = [account['username'] for account in results]
		if session['username'] in results:
			results.remove(session['username'])
		return json.dumps(results)
	# handle src submission
	elif request.form['action'] == 'submit-code': 
		game = db.getGame(int(request.form['game_id']))
		player_id = game['players'].index(session['username'])

		# if the player hasn't already submitted src
		if int(game['turn']) > len(game['srces'][player_id]):
			# submit his src
			game['srces'][player_id].append(request.form['src'])
			game_data = {'srces': game['srces']}
			db.updateGame(int(request.form['game_id']), game_data)
		return "sonofabitch" # tryna submit mo src
	# return a player's point of view in a given game
	elif request.form['action'] == 'get-json':
		game = db.getGame(int(request.form['game_id']))
		player_id = game['players'].index(session['username'])

		return json.dumps({'jsons': game['jsons'][player_id]})

@app.route('/easter/geocities/<value>')
def geocities(value):
	if value == "on":
		session["geocities"] = True
		flash("Geocities mode activated!")
	else:
		if "geocities" in session:
			session.pop("geocities")
			flash("Geocities mode deactivated!")
	return redirect(url_for('home'))

@app.route('/events')
def events():
	f = open('static/json/events.json')
	t = f.read();
	f.close()
	return "{\"events\": []}"

@app.route('/gamedemo', methods=['POST'])
def gamedemo():
    w = world2.World(100, 100)
    for i in xrange(50):
	unit = world2.Unit(0,0,0,10)
	id = w.add_unit(unit)
	unit.vx = random.randint(1,2);
	unit.vy = random.randint(-1,1);
	w.add_event("ActorVelocityChange", {'id': id,
	    'x': unit.x,
	    'y': unit.y,
	    'vx': unit.vx,
	    'vy': unit.vy})
    for i in xrange(50):
	unit = world2.Unit(300,0,1,10)
	id = w.add_unit(unit)
	unit.vx = random.randint(-2,-1);
	unit.vy = random.randint(-1,1);
	w.add_event("ActorVelocityChange", {'id': id,
	    'x': unit.x,
	    'y': unit.y,
	    'vx': unit.vx,
	    'vy': unit.vy})
    for i in xrange(250):
	print "step",i
	w.step()
    return w.serialized_events()


if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
