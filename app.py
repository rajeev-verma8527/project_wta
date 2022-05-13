from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

#ye hai ek

@app.route("/data")
def data():
    pass
