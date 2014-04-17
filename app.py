from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("home.html")

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
