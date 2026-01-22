# -*- coding: utf-8 -*-

from flask import (
    Flask,
    request,
    json,
    render_template,
    make_response,
    redirect,
    url_for,
    jsonify,
    json,
    session,
    send_file
)
import requests
import json
import yagmail
from flask_session import Session
import os
from pathlib import Path
from src.objects.Application import Application, get_data
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, base64
from datetime import datetime, timedelta
from src.server.flask_server import app, db
from src.sql.sqlite import User
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.src_context import root_dir
from smtplib import SMTPAuthenticationError
from functools import wraps
from flasgger import Swagger, swag_from
from src.common.utils import send_mail
# from PythonResumeBuilder.generate_resume import generate_online_resume



load_dotenv(os.path.join(root_dir, ".env"))
# Get the absolute path of the current file
current_file_path = Path(__file__).resolve()

# Get the directory of the current file
current_dir = current_file_path.parent
# resume_builder_dir
resume_builder_dir = os.path.join(current_dir, "PythonResumeBuilder")
# creates Flask object
app = Flask(__name__, static_folder=os.path.join(root_dir, "images"))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)

swagger = Swagger(app)

# Declare the variables
greetings_map = {
    "Good Morning!": list(range(0, 12)),
    "Good Afternoon!": list(range(12, 16)),
    "Good Evening!": list(range(16, 24)),
}

main_dir = os.getcwd()
resume_file_path = main_dir + "/docs"
resume_file = os.path.join(resume_file_path, "Resume.pdf")
image_folder = os.path.join(main_dir, "images")
template_folder = os.path.join(main_dir, "templates")
body = os.path.join(image_folder, "one_page_profile.png")
html_msg = [
    yagmail.inline(body),
    os.path.join(template_folder, "links.html"),
    resume_file,
]

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login_post"))

    return wrap


app.config["DEBUG"] = True
SESSION_TYPE = "filesystem"
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
@swag_from('api_routes.yml', endpoint='login')
@app.route("/login", endpoint='login', methods=["GET", "POST"])
def login_post():
    if request.method == "GET":
        return render_template("login.html", msg="")
    else:
        msg = ""
        # creates dictionary of form data
        auth = request.args if request.args else request.form

        session_time = (
            auth.get("session_time") if auth.get("session_time") != None else 30
        )
        if not auth or not auth.get("email") or not auth.get("password"):
            # returns 401 if any email or / and password is missing
            return make_response(
                "Could not verify",
                401,
                {"WWW-Authenticate": 'Basic realm ="Login required !!"'},
            )
        user = User.query.filter_by(email=auth.get("email")).first()
        if not user:
            # returns 401 if user does not exist
            return make_response(
                "Could not verify",
                401,
                {"WWW-Authenticate": 'Basic realm ="User does not exist !!"'},
            )
        if check_password_hash(user.password, auth.get("password")):
            # generates the JWT Token
            token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.utcnow() + timedelta(days=session_time),
                },
                key = "secret"
            )
            session["user"] = auth.get("email")
            session["logged_in"] = True
            session["username"] = user.name
            # return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
            return render_template(
                "user_form.html",
                msg="Hi {}! How are you doing today?".format(session["username"]),
            )

        # returns 403 if password is wrong
        msg = "Please provide correct credentials. Incase you forget password, please click on forget password."
        return render_template("login.html", msg=msg)


@app.route("/password_reset", methods=["GET", "POST"])
@swag_from()
def reset_password():

    if request.method == "GET":
        msg = ""
        return render_template("password_reset.html", msg=msg)
    elif request.method == "POST":
        auth = request.args if request.args else request.form
        print(request.form)
        user = User.query.filter_by(email=auth.get("email")).first()

        if not user:
            print(user)
            # returns 401 if user does not exist
            msg = "User does not exist !!"
            return render_template("password_reset.html", msg=msg)
        else:
            secret_key = user.password.split("$")[1]
            passw = os.getenv("passwd")
            yagmail.register("richie.chatterjee31@gmail.com", passw)
            yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
            html_msg = [
                yagmail.inline(
                    """
                Secret Key: {},
                Password Recovery Link:{}
                """.format(
                        secret_key, "http://127.0.0.1:5001/new_password"
                    )
                ),
            ]
            """Send Email"""
            session["user"] = auth.get("email")
            yag.send(auth.get("email"), "NotifyApp_Password_Recovery_Link", html_msg)
            msg = "Email has been sent to the registered email address {} with temporary password.".format(
                session["user"]
            )

            return render_template("set_new_password.html", msg=msg)

@swag_from('api_routes.yml', endpoint='/new_password')
@app.route("/new_password", methods=["GET", "POST"])
def new_password():
    if request.method == "GET":
        return render_template("set_new_password.html")
    elif request.method == "POST":
        auth = request.args if request.args else request.form
        user = User.query.filter_by(email=session["user"]).first()
        if auth.get("secret") == user.password.split("$")[1]:
            # todo update the user table with new password.
            password_user = generate_password_hash(auth.get("new_password"))
            db.session.query(User).filter_by(email=session["user"]).update(
                {"password": password_user}
            )
            db.session.commit()
            msg = "password updated for {}".format(session["user"])
        else:
            msg = "Incorrect secret token"
            return render_template("set_new_password.html", msg=msg)
        return render_template("login.html", msg=msg)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("login.html", msg="")
    if request.method == "POST":
        # creates a dictionary of the form data
        data = request.args if request.args else request.form
        # gets name, email and password
        name, email = data.get("username"), data.get("email")
        password = data.get("password")
        # checking for existing user
        user = User.query.filter_by(email=email).first()
        if not user:
            password_user = generate_password_hash(password)
            user = User(
                public_id=str(uuid.uuid4()),
                name=name,
                email=email,
                password=password_user,
                created=datetime.now(),
            )
            # insert user
            db.session.add(user)
            db.session.commit()
            return render_template(
                "login.html",
                msg="Hi {}, you are now registered with notify application.".format(
                    user.name
                ),
            )
        else:
            # returns 202 if user already exists
            return render_template(
                "login.html",
                msg="User already exists. Please Log in. In case you forgot password, please click on forgot password password.",
            )


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    msg = "You have been logged out!"
    return render_template("login.html", msg=msg)


@app.route("/application_history")
@login_required
def application_history():
    return redirect(plot_url)

@swag_from('api_routes.yml', endpoint='user_profile')
@app.route("/user_profile", endpoint='user_profile',  methods=["GET"])
@login_required
def user_profile():
    if request.method == "GET":
        greeting = [k for k, v in greetings_map.items() if datetime.now().hour in v]
        msg = "Hi {}. {}".format(session["username"], greeting[0])
        user = User.query.filter_by(email=session["user"]).first()
        urls = []
        project_names = []
        image = None
        about_me = user.about_me
        try:
            git = eval(user.git)
            urls.append(git["url"])
            project_names.append(git["name"])
        except KeyError:
            pass
        try:
            image = base64.b64encode(user.image).decode("ascii")
        except TypeError:
            pass
        try:
            projects = eval(user.projects)
            project_names.append(
                projects["project1"]["name"])
            urls.append(projects["project1"]["url"])
        except KeyError:
            pass
        try:
            projects = eval(user.projects)
            project_names.append(
                projects["project2"]["name"])
            urls.append(projects["project2"]["url"])
        except KeyError:
            pass

        return render_template(
            "profile.html",
            msg=msg,
            project_names=project_names,
            urls=urls,
            len=len(project_names),
            data=list,
            image=image,
            about_me=about_me,
        )


@app.route("/update", methods=["POST"])
def update():
    data = request.form
    try:
        if data["cache"] == "clear cache":
            Application.all_contacts = []
        else:
            Application.update("update")
            # post update clear the cache
            print("Clearing the cache post update.")
            Application.all_contacts = []
        return render_template("user_form.html")
    except KeyError:
        Application.update("update")
        # post update clear the cache
        print("Clearing the cache post update.")
        Application.all_contacts = []
        return render_template("user_form.html")


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    greeting = [k for k, v in greetings_map.items() if datetime.now().hour in v]
    msg = "Hi {}. {}".format(session["username"], greeting[0])
    return render_template("user_form.html", msg=msg)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    greeting = [k for k, v in greetings_map.items() if datetime.now().hour in v]
    msg = "Hi {}. {}".format(session["username"], greeting[0])
    if request.method == "GET":
        message = {"msg": msg, "response": ""}
        return render_template("settings.html", message=message)

    elif request.method == "POST":
        data = request.files
        if data["image"].filename != "":
            db.session.query(User).filter_by(email=session["user"]).update(
                {"image": data["image"].read()}
            )
            db.session.commit()
        if data["resume"].filename != "":
            db.session.query(User).filter_by(email=session["user"]).update(
                {"resume": data["resume"].read()}
            )
            print("saving the pdf")
            db.session.commit()
        if data["profile"].filename != "":
            db.session.query(User).filter_by(email=session["user"]).update(
                {"profile": data["profile"].read()}
            )
            db.session.commit()
        message = {"msg": msg, "response": "Details saved successfully."}
        return render_template("settings.html", message=message)


@app.route("/screenshot", methods=["GET"])
def screenshot():
    return render_template("screenshot.html")


@app.route("/project_details", methods=["POST"])
def project_details():
    data = request.form
    if "about_me" in data.keys():
        db.session.query(User).filter_by(email=session["user"]).update(
            {"about_me": data["about_me"]}
        )
        db.session.commit()
    if "Git" in data.keys():
        if data["Git"] == '':
            pass
        else:
            git = json.dumps({"name": "Git", "url": data["Git"]})
            db.session.query(User).filter_by(email=session["user"]).update({"git": git})
            db.session.commit()
    projects = {}
    if "project1" in data.keys() and data["project1"] != '':
        projects.update({"project1": {"name": data["project1"], "url": data["project1_url"]}})
    if "project2" in data.keys() and data["project2"] != '':
        projects.update({"project2": {"name": data["project2"], "url": data["project2_url"]}})

    db_proj = db.session.query(User).filter_by(email=session["user"]).first()
    if db_proj.projects is not None:
        db_dict =eval(db_proj.projects)
        db_dict.update(projects)
        db.session.query(User).filter_by(email=session["user"]).update(
            {"projects": json.dumps(db_dict)})
        db.session.commit()
    else:
        db.session.query(User).filter_by(email=session["user"]).update(
            {"projects": json.dumps(projects)})
        db.session.commit()

    greeting = [k for k, v in greetings_map.items() if datetime.now().hour in v]
    msg = "Hi {}. {}".format(session["username"], greeting[0])
    message = {"msg": msg, "response": "Details saved successfully."}
    return render_template("settings.html", message=message)


@app.route("/addDetails", methods=["POST"])
def addDetails():
    data = request.form
    if data["resume"]:
        resume_file = data["resume"]
        html_msg = [
            yagmail.inline(body),
            os.path.join(template_folder, "links.html"),
            resume_file,
        ]
    # Instantiate the Application object and execute required method.
    obj = Application(data)
    obj.add_details()
    email = data["Email Address"]
    response = send_mail("richie.chatterjee31@gmail.com", 
              os.getenv("passwd"), 
              "richie.chatterjee31@gmail.com", 
              obj.subject, 
              html_msg=html_msg)
    return render_template("user_form_response.html", msg="Successfully Submitted")


@app.route("/application_details", methods=["GET"])
@login_required
def application_details():
    return render_template("application_table.html")


@app.route("/check_cache", methods=["GET", "POST"])
@login_required
def check_cache():
    if request.method == "GET":
        msg = Application.all_contacts
        return render_template("cache.html", len=len(msg), msg=msg)
    if request.method == "POST":
        data = request.form.getlist("cache")
        msg = Application.all_contacts
        # determine indexes to delete from Application instance based on user input.
        index = []
        email_list = [msg[i].email for i in range(len(msg))]
        for email in data:
            index.append(email_list.index(email))
        # delete the indexes,
        for i in index:
            msg.pop(i)
        return render_template("cache.html", len=len(msg), msg=msg)


@app.route("/delete_form", methods=["GET"])
@login_required
def delete_form():
    return render_template("delete_details.html")


@app.route("/get_data", methods=["GET"])
@login_required
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

@app.route("/job_details", methods=["GET"])
@login_required
def job_details():
    collection = []
    job_posting_data = requests.get(os.getenv("job_api_url"))
    job_data=json.loads(job_posting_data.content.decode("utf-8"))
    columns = list(json.loads(job_data["data"][0]).keys())
    for iter_ in range(len(job_data["data"])):
        iter_data = json.loads(job_data["data"][iter_])
        row_values = [list(iter_data.values()) for i in range(len(iter_data))]
        # unpack the values in row_values
        # find number of values to iterate through
        for row in range(len(row_values[0][0])):
            values = [row_values[0][i][row] for i in range(len(row_values[0]))]
            collection.append(dict(zip(columns, values)))
    # Retrieve existing data from cache
    data = {"data": collection}
    return jsonify(data)

@app.route('/show_jobs', methods=['GET'])
@login_required
def show_jobs():
    return render_template('job_posting.html')

@app.route('/apply_job', methods=['POST'])
def apply_job():
    data = request.get_json()
    # renaming the keys
    data["Company"] = data.pop("Company_Name")
    data["Email Address"] = data.pop("Email_Address")
    data["Subject"] = ""
    obj = Application(data)
    obj.add_details()
    response = send_mail('richie.chatterjee31@gmail.com',
              os.getenv("passwd"), 
              data["Email Address"], 
              obj.subject, 
              html_msg=html_msg)
    return render_template('job_posting.html', msg=response)


@app.route('/render_resume_builder', methods=['GET'])
def render_resume_builder():
    # Load default data from files
    with open(os.path.join(resume_builder_dir,'resume.json'), 'r') as f:
        DEFAULT_JSON = f.read()

    with open(os.path.join(resume_builder_dir,'template.html'), 'r') as f:
        DEFAULT_HTML = f.read()
    return render_template("resume_builder.html", default_json=DEFAULT_JSON, default_html=DEFAULT_HTML)

# @app.route('/build-resume', methods=['POST'])
# def build_resume():
#     """
#     Receives JSON and HTML from the client and "builds" the resume on the server.
#     """
#     try:
#         from jinja2 import Environment, FileSystemLoader

#         # === Server-side resume building logic ===
#         data = request.get_json()
#         json_data = json.loads(data.get('jsonData'))
#         html_template = data.get('htmlTemplate')
#         env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))
#         template = env.from_string(html_template)
#         pdf_data = generate_online_resume(json_data, template, "resume.pdf")

#         return send_file(
#             pdf_data,
#             mimetype='application/pdf',
#             as_attachment=True,
#             download_name='resume.pdf'
#         )
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("port"))
