from flask import Flask, render_template, request
app = Flask(__name__)

app.debug=False

@app.route('/')
def hello():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/data")
def data():
    pass
