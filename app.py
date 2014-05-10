from flask import Flask, render_template, session, request, redirect, url_for, flash
import db

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/')
def home():
    d = {'logged_in': 'username' in session}
    return render_template("home.html", d=d)

@app.route('/register', methods=["GET","POST"])
def register():
	d = {"errors": []}
	d['logged_in'] = 'username' in session
	if request.method == "GET":
		return render_template("register.html", d=d)
	
	# POST
	errors = db.create_account(request.form)
	if errors:
		d['errors'] = errors
		return render_template("register.html", d=d)

	# no errors
	session['username'] = request.form['username']
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect(url_for('home'))

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
    return render_template("versus.html", d=d)

@app.route('/learn/')
def learn():
    d = {'logged_in': 'username' in session}
    return render_template("learn.html", d=d)

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

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
