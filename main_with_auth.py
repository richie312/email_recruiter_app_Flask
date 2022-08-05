# -*- coding: utf-8 -*-

from flask import (
    Flask,
    request,
    json,
    render_template,
    redirect,
    url_for,
    jsonify,
    json,
)
import yagmail
from dotenv import load_dotenv
from flask import Flask, session
from flask_session import Session
import os
from src.objects.Application import Application, get_data
from flask import Flask, request, jsonify, make_response, render_template
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import jwt
from datetime import datetime, timedelta
from src.server.flask_server import app, db
from src.Auth.Authentication import token_required
from src.sql.sqlite import User
from src.objects.Application import Application
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.src_context import root_dir
from smtplib import SMTPAuthenticationError

load_dotenv(os.path.join(root_dir, '.env'))

# creates Flask object
app = Flask(__name__,static_folder=os.path.join(root_dir,'images'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
print(db)

app.config['DEBUG'] = True
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# load the environment variables
load_dotenv(".env")
port = os.getenv("port")
plot_url = os.getenv("plot_url")


@app.route("/")  # Standard Flask endpoint
def homepage():
    return render_template("login.html")

# route for logging user in
@app.route('/login', methods=['GET','POST'])
def login_post():
    if request.method == 'GET':
        return render_template("login.html", msg = "")
    else:
        msg = ""
        # creates dictionary of form data
        auth = request.args if request.args else request.form

        session_time = auth.get("session_time") if auth.get("session_time") != None else 30
        if not auth or not auth.get('email') or not auth.get('password'):
            # returns 401 if any email or / and password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )
        user = User.query \
            .filter_by(email=auth.get('email')) \
            .first()
        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )
        if check_password_hash(user.password, auth.get('password')):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(days=session_time)
            }, app.config['SECRET_KEY'])
            session["user"] = auth.get("email")
            #return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
            return render_template("user_form.html", msg= "Hi {}! How are you doing today?".format(session["user"].split('@')[0]))

        #returns 403 if password is wrong
        msg = "Please provide correct credentials. Incase you forget password, please click on forget password."
        return render_template("login.html", msg = msg)



@app.route("/password_reset", methods = ["GET","POST"])
def reset_password():

    if request.method == 'GET':
        msg = ''
        return render_template("password_reset.html", msg=msg)
    elif request.method == 'POST':
        auth = request.args if request.args else request.form
        print(request.form)
        user = User.query \
            .filter_by(email=auth.get('email'))\
            .first()

        if not user:
            print(user)
            # returns 401 if user does not exist
            msg = 'User does not exist !!'
            return render_template("password_reset.html", msg = msg)
        else:
            secret_key = user.password.split('$')[1]
            passw = os.getenv("passwd")
            yagmail.register("richie.chatterjee31@gmail.com", passw)
            yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
            html_msg = [
                yagmail.inline("""
                Secret Key: {},
                Password Recovery Link:{}  
                """.format(secret_key, 'http://127.0.0.1:5001/new_password' )),
            ]
            """Send Email"""
            session["user"] = auth.get("email")
            yag.send(auth.get('email'), "NotifyApp_Password_Recovery_Link", html_msg)
            msg = "Email has been sent to the registered email address {} with temporary password.".format(session["user"])

            return render_template("set_new_password.html", msg = msg)



@app.route('/new_password', methods = ['GET', 'POST'])
def new_password():
    if request.method == 'GET':
        return render_template("set_new_password.html")
    elif request.method == 'POST':
        auth = request.args if request.args else request.form
        user = User.query.filter_by(email=session["user"]).first()
        if auth.get('secret') == user.password.split('$')[1]:
            # todo update the user table with new password.
            password_user = generate_password_hash(auth.get("new_password"))
            db.session.query(User).filter_by(email=session["user"]).update({"password": password_user})
            db.session.commit()
            msg = "password updated for {}".format(session["user"])
        else:
            msg = "Incorrect secret token"
            return render_template("set_new_password.html", msg=msg)
        return render_template("login.html", msg = msg)


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("login.html", msg = "")
    if request.method == 'POST':
        # creates a dictionary of the form data
        data = request.args if request.args else request.form
        # gets name, email and password
        name, email = data.get('name'), data.get('email')
        password = data.get('password')
        # checking for existing user
        user = User.query \
            .filter_by(email=email) \
            .first()
        if not user:
            password_user = generate_password_hash(password)
            user = User(
                public_id=str(uuid.uuid4()),
                name=name,
                email=email,
                password= password_user,
                created = datetime.now()
            )
            # insert user
            db.session.add(user)
            db.session.commit()
            return render_template("login.html", msg = "Hi {}, you are now registered with notify application.".format(user.name))
        else:
            # returns 202 if user already exists
            return render_template("login.html",msg = "User already exists. Please Log in. In case you forgot password, please click on forgot password password.")







@app.route("/application_history")
@login_required
def application_history():
    return redirect(plot_url)


@app.route("/update", methods=["POST"])
def update():
    data = request.form
    if data["cache"] == "clear cache":
        Application.all_contacts = []
    else:
        Application.update("update")
        # post update clear the cache
        print("Clearing the cache post update.")
        Application.all_contacts = []
    return render_template("user_form_response.html")


@app.route("/addDetails", methods=["POST"])
def addDetails():
    data = request.form
    passw = data["Password"]
    main_dir = os.getcwd()
    image_folder = os.path.join(main_dir, "images")
    template_folder = os.path.join(main_dir, "templates")
    html_msg = [
        yagmail.inline(os.path.join(image_folder, "one_page_profile.png")),
        os.path.join(template_folder, "links.html"),
        main_dir + "/docs/Resume.pdf",
    ]
    # Instantiate the Application object and execute required method.
    obj = Application(data)
    email = data["Email Address"]

    try:
        yagmail.register(session["user"], passw)
        yag = yagmail.SMTP(session["user"], passw)
        """Send Email"""
        yag.send(email, obj.subject, html_msg)
    except SMTPAuthenticationError:
        yagmail.register("richie.chatterjee31@gmail.com", passw)
        yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
        """Send Email"""
        yag.send(to = [email, session["user"]], obj.subject, html_msg)
    return render_template("user_form_response.html")


@app.route("/application_details", methods=["GET"])
def application_details():
    return render_template("application_table.html")


@app.route("/delete_form", methods=["GET"])
def delete_form():
    return render_template("delete_details.html")


@app.route("/get_data", methods=["GET"])
def data():
    data = get_data()
    return jsonify(data)


@app.route("/delete", methods=["POST"])
def delete():
    templateData = {}
    data = request.form
    print(data)
    Application(data).delete()
    templateData["redirect_url"] = url_for("application_details")
    return render_template("delete_details_response.html", **templateData)


@app.route("/index_get_data", methods=["GET"])
def populate_data():
    response = get_data()
    columns = [response["col"][i][0] for i in range(len(response["col"]))]
    collection = [
        dict(zip(columns, response["data"][i])) for i in range(len(response["data"]))
    ]
    data = {"data": collection}
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
