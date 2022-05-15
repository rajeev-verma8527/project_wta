from flask import (
    Flask,
    render_template,
    request,
    make_response,
    jsonify,
    url_for,
    send_file,
    Response,
)
import json

app = Flask(__name__)
import datetime

# def readfile():
#     lines = []
#     with open("data.txt", "r") as file:
#         lines = file.readlines()
#     return lines


@app.route("/")
def hello():
    s = f"{request.referrer=} {request.remote_addr=} {request.environ['REMOTE_ADDR']=} {request.environ['HTTP_X_FORWARDED_FOR']=}"
    return s


# @app.route("/dashboard", methods=["GET", "POST"])
# def dashboard():
#     if request.method == "POST":
#         print(request.form.get("name"))
#     return render_template("dashboard.html")


# @app.route("/args")
# def args():
#     with open("data.txt", "a") as file:
#         file.write("ARGS:")
#         file.write(" ".join((f"{key}={val}" for key, val in request.args.items())))
#         file.write("\n")
#     return "<br>".join(readfile())


# @app.route("/post", methods=["GET", "POST", "OPTIONS"])
# def post():
#     if request.method == "OPTIONS":
#         r = make_response()
#         r.headers.add("Access-Control-Allow-Headers", "*")
#         r.headers.add("Access-Control-Allow-Origin" , "http://127.0.0.1:5500")
#         return r
#     if request.method == "POST":
#         # print(request.headers)
#         # print(request.json["location"])
#         # print(json.loads(request.get_data()))
#         # with open("data.txt", "a") as file:
#         #     file.write("post:")
#         #     file.write(request.form.get("json"))
#         #     file.write("\n")
#         r = make_response()
#         r.headers.add("Access-Control-Allow-Origin" , "http://127.0.0.1:5500")
#         return r
#     else:
#         return "<br>".join(readfile())


# @app.route("/js")
# def js():
#     print(request.remote_addr)
#     print(request.environ['REMOTE_ADDR'])
#     return send_file("static/script.js",mimetype="text/javascript")
