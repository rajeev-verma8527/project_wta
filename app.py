from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    make_response,
    flash,
    send_file,
    send_from_directory
)
import os
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

import datetime
from database import db_session, PageVisit, User
from verification import verify_user, domain_exists

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.getenv("flask_key")

login_manager.login_view = "login"
login_manager.login_message = "Login Required"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    with db_session() as sess:
        user = sess.query(User).get(user_id)
    return user


@app.route("/raw")
@login_required
def raw():
    ctx = {}
    with db_session() as db:
        ctx["data"] = db.query(PageVisit).all()
    return render_template("raw.html", ctx=ctx)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if user := verify_user(username, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Username or Passoword", category="warning")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/data", methods=["POST", "OPTIONS"])
def data():  # can send json data via POST request and only by saved domains
    try:
        if not domain_exists(request.origin):
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
        # print("data rec",data)
        with db_session() as sess:
            obj = PageVisit(
                page=data["page"],
                referer=data["referer"],
                loadtime=data["loadTime"],
                ip=data["ipAddress"],
                country=data["country"],
                countryCode=data["countryCode"],
                state=data["state"],
                city=data["city"],
                time=datetime.datetime.utcfromtimestamp(data["unixSeconds"]),
            )
            sess.add(obj)
            sess.commit()
            # flash(f"Data received from website {datetime.datetime.utcfromtimestamp(data['unixSeconds'])}")
        resp = make_response()
        resp.headers.add("Access-Control-Allow-Origin", request.origin)
        resp.status_code = 201

        return resp

    return make_response(), 501


@app.route("/script")
def script():
    return render_template("script.js"), {"Content-Type": "text/javascript"}

@app.route("/database")
@login_required
def database():
    return send_from_directory("","data_db.sqlite3")

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
