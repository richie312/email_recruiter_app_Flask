# -*- coding: utf-8 -*-

from flask import Flask, request,render_template,redirect,url_for,jsonify,session
import yagmail, requests, json
from dotenv import load_dotenv
from datetime import datetime
import os
from smtplib import SMTPAuthenticationError
from src.objects.Application import Application, get_data
from src.common.utils import send_mail
from flask_login import current_user
app = Flask(__name__)


# load the environment variables
load_dotenv('.env')
port = os.getenv('port')
plot_url = os.getenv('plot_url')

# variable declarations
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

@app.route("/")        # Standard Flask endpoint
def homepage():
    return render_template("user_form.html")


@app.route("/application_history")
def application_history():
    return redirect(plot_url)


@app.route('/addDetails', methods=['POST'])
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
    return render_template("user_form_response.html", msg=response)

@app.route('/apply_job', methods=['POST'])
def apply_job():
    data = request.get_json()
    # renaming the keys
    data["Company"] = data.pop("Company_Name")
    data["Email Address"] = data.pop("Email_Address")
    data["Subject"] = ""
    obj = Application(data)
    obj.add_details()
    response = send_mail("richie.chatterjee31@gmail.com", 
              os.getenv("passwd"), 
              "richie.chatterjee31@gmail.com", 
              obj.subject, 
              html_msg=html_msg)
    return render_template('job_posting.html', msg=response)

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

@app.route("/job_details", methods=["GET"])
def job_details():
    collection = []
    job_posting_data = requests.get("http://192.168.1.4:5003/consume")
    job_data=json.loads(job_posting_data.content.decode("utf-8"))
    columns = list(json.loads(job_data["data"][0]).keys())
    for iter_ in range(len(job_data["data"])):
        iter_data = json.loads(job_data["data"][iter_])
        row_values = [list(iter_data.values()) for i in range(len(iter_data))]
        # unpack the values in row_values
        for row in range(len(row_values[0])):
            values = [row_values[0][i][row-1] for i in range(len(row_values[0]))]
            collection.append(dict(zip(columns, values)))
    # Retrieve existing data from cache
    data = {"data": collection}
    return jsonify(data)

@app.route('/show_jobs', methods=['GET'])
def show_jobs():
    return render_template('job_posting.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5000)