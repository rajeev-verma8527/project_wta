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
import os
import datetime
from database import db_session, PageVisits, Websites, Login, Session, DATABASE_PATH
from sqlalchemy import select
import pandas as pd

app = Flask(__name__)

app.secret_key = os.getenv("flask_key")


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/data", methods=["POST", "OPTIONS"])
def data():  # can send json data via POST request and only by saved domains
    try:
        q = select(Websites).filter_by(domain=request.origin)
        with db_session() as sess:
            if not sess.scalar(q):
                return make_response(), 403
    except:
        return make_response(), 500

    if request.method == "OPTIONS":
        resp = make_response()
        resp.headers.add("Access-Control-Allow-Headers", "*")
        resp.headers.add("Access-Control-Allow-Origin", request.origin)
        return resp

    if request.method == "POST":
        data = request.json
        print("data rec",data)
        obj = PageVisits(
            page = data["page"],
            referer = data['referer'],
            loadtime = data['loadTime'],
            ip = data['ipAddress'],
            country = data['country'],
            countryCode = data['countryCode'],
            state = data['state'],
            city = data['city'],
            time = datetime.datetime.utcfromtimestamp(data['unixSeconds'])
        )

        with db_session() as sess:
            sess.add(obj)
            sess.commit()

        df= pd.read_sql_table("page_visits",DATABASE_PATH)
        df.to_html(r"templates\pdout.html",classes="table")

        resp = make_response()
        resp.headers.add("Access-Control-Allow-Origin", request.origin)
        resp.status_code = 201

        return resp

    return make_response(),501


@app.route("/script")
def script():
    return render_template("script.js"), {"Content-Type": "text/javascript"}


# @app.route("/js")
# def js():
#     return send_file("static/script.js", mimetype="text/javascript")

# @app.route("/args")
# def args():
#     with open("data.txt", "a") as file:
#         file.write("ARGS:")
#         file.write(" ".join((f"{key}={val}" for key, val in request.args.items())))
#         file.write("\n")
#     return "<br>".join(readfile())
