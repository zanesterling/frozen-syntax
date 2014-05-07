from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/')
def home():
    return render_template("home.html")

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

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
