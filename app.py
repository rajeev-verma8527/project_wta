from flask import Flask, render_template, request
app = Flask(__name__)

app.debug=False

@app.route('/')
def hello():
    return render_template("index.html")
