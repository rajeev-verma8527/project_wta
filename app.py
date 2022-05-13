from flask import Flask, render_template, request
app = Flask(__name__)
import datetime

def readfile():
    lines = []
    with open("data.txt",'r') as file:
        lines = file.readlines()
    return lines

@app.route('/')
def hello():
    return render_template("index.html")


@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    if request.method == "POST":
        print(request.form.get("name"))
    return render_template("dashboard.html")

@app.route("/args")
def args():
    with open("data.txt","a") as file:
        file.write("ARGS:" )
        file.write(" ".join((f"{key}={val}" for key,val in request.args.items())))
        file.write("\n")
    return "<br>".join(readfile())


@app.route("/post", methods=["GET","POST"])
def post():
    if request.method == "POST":
        # print(request.form.get("json"))
        with open("data.txt","a") as file:
            file.write("post:" )
            file.write(request.form.get("json"))
            file.write("\n")
    return "<br>".join(readfile())