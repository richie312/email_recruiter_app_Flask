# -*- coding: utf-8 -*-

from flask import Flask, request,render_template,redirect,url_for,jsonify,session
import yagmail
from dotenv import load_dotenv
from datetime import datetime
import os
from smtplib import SMTPAuthenticationError
from src.objects.Application import Application, get_data
app = Flask(__name__)
app.config['DEBUG'] = True

# load the environment variables
load_dotenv('.env')
port = os.getenv('port')
plot_url = os.getenv('plot_url')


greetings_map = {
    "Good Morning!": list(range(0, 12)),
    "Good Afternoon!": list(range(12, 16)),
    "Good Evening!": list(range(16, 24)),
}


@app.route("/")        # Standard Flask endpoint
def homepage():
    return render_template("user_form.html")


@app.route("/application_history")
def application_history():
    return redirect(plot_url)


# @app.route('/addDetails', methods=['POST'])
# def addDetails():
#     data = request.form
#     passw = data['Password']
#     main_dir = os.getcwd()
#     yagmail.register("richie.chatterjee31@gmail.com", passw)
#     yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
#     image_folder = os.path.join(main_dir,'images')
#     template_folder = os.path.join(main_dir,'templates')
#     html_msg = [yagmail.inline(os.path.join(image_folder,"profile2.jpg")),
#     os.path.join(template_folder,"links.html"),
#     main_dir + "/docs/Resume.pdf"]
#     # Instantiate the Application object and execute required method.
#     obj = Application(data)
#     # Insert data
#     obj.add_details()
#     email = data['Email Address']
#     """Send Email"""
#     yag.send(email, obj.subject, html_msg)
#     return render_template('user_form_response.html')

@app.route('/addDetails', methods=['POST'])
def addDetails():
    data = request.form
    passw = data["Password"]
    main_dir = os.getcwd()
    if data["resume"]:
        resume_file = data["resume"]
        resume_file_path = main_dir + "/docs"
    else:
        user = "richie312"
        resume_file = main_dir + "/docs/Resume.pdf"
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
    # Instantiate the Application object and execute required method.
    obj = Application(data)
    email = data["Email Address"]

    try:
        yagmail.register("richie.chatterjee31@gmail.com", passw)
        yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
        """Send Email"""
        yag.send(email, obj.subject, html_msg)
        msg = ""
        return render_template("user_form_response.html", msg=msg)
    except SMTPAuthenticationError:
        yagmail.register("richie.chatterjee31@gmail.com", os.getenv("passwd"))
        yag = yagmail.SMTP("richie.chatterjee31@gmail.com", os.getenv("passwd"))
        """Send Email"""
        yag.send([email, "richie.chatterjee31@gmail.com"], obj.subject, html_msg)
        msg = """Alert! Hi {}.As your google password is not set, the mail is by default sent by domain owner.
                It is recommended that you use gmail account and set google app password.
                Click on the Set google app password button on dashboard to set it up.""".format(
            "testaccount"
        )
    return render_template("user_form_response.html", msg=msg)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    greeting = [k for k, v in greetings_map.items() if datetime.now().hour in v]
    msg = "Hi {}. {}".format("Richie", greeting[0])
    return render_template("user_form.html", msg=msg)

@app.route('/application_details', methods=['GET'])
def application_details():
    return render_template('application_table.html')

@app.route('/delete_form', methods=['GET'])
def delete_form():
    return render_template('delete_details.html')

@app.route('/get_data', methods=['GET'])
def data():
    data = get_data()
    return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete():
    templateData = {}
    data = request.form
    Application(None).delete(data["Company"])
    templateData['redirect_url'] = url_for('application_details')
    return render_template('delete_details_response.html',**templateData)

@app.route('/index_get_data', methods=['GET'])
def populate_data():
    response = get_data()
    columns = [response['col'][i][0] for i in range(len(response['col']))]
    collection = [dict(zip(columns, response['data'][i])) for i in range(len(response['data']))]
    data = {"data": collection}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)