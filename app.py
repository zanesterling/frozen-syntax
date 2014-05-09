from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=["GET","POST"])
def register():
	d = {"errors": []}
	if request.method == "GET":
		return render_template("register.html", d=d)
	
	# POST
	errors = db.createAccount(request.form)
	if errors:
		d['errors'] = errors
		return render_template("register.html", d=d)

	login(request.form['username'])
	return redirect(url_for('home'))

@app.route('/play/')
def play():
    return render_template("play.html")

@app.route('/play/solo/')
def solo():
    return render_template("solo.html")

@app.route('/play/versus/')
def versus():
    return render_template("versus.html")

@app.route('/learn/')
def learn():
    return render_template("learn.html")

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
