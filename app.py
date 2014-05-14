from flask import Flask, render_template, session, request, redirect, url_for, flash
import json
import md5
import error
import db

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
    d['hashed_email'] = md5.new(d['user_info']['email'].lower()).hexdigest()
    games = db.getActiveGames()
    gameslist = []
    for game in games:
        if username in game['players']:
            game['players'] = [db.getInfo(user) for user in game['players']]
            for player in game['players']:
                player['hashed_email'] = md5.new(player['email'].lower()).hexdigest()
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

@app.route('/learn/')
def learn():
    d = {'logged_in': 'username' in session}
    return render_template("learn.html", d=d)

@app.route('/action', methods=["POST"])
def action():
    if request.form['action'] == 'match-username':
        results = db.matchUsername(request.form['username'])
        results = [account['username'] for account in results]
        if session['username'] in results:
            results.remove(session['username'])
        return json.dumps(results)

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

@app.route('/graphics')
def graphics():
	return render_template("graphics.html")

@app.route('/events')
def events():
	f = open('static/json/events.json')
	t = f.read();
	f.close()
	return t

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
