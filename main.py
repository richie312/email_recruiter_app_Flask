# -*- coding: utf-8 -*-

from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
import yagmail
from dotenv import load_dotenv
import os
from src.objects.Application import Application, get_data
app = Flask(__name__)
app.config['DEBUG'] = True

# load the environment variables
load_dotenv('.env')
port = os.getenv('port')
plot_url = os.getenv('plot_url')

@app.route("/")        # Standard Flask endpoint
def homepage():
    return render_template("user_form.html")


@app.route("/application_history")
def application_history():
    return redirect(plot_url)

@app.route('/update', methods=['POST'])
def update():
    data = request.form
    if data["cache"] == "clear cache":
        Application.all_contacts = []
    else:
        Application.update("update")
        #post update clear the cache
        print("Clearing the cache post update.")
        Application.all_contacts = []
    return render_template('user_form_response.html')

@app.route('/addDetails', methods=['POST'])
def addDetails():
    data = request.form
    passw = data['Password']
    main_dir = os.getcwd()
    yagmail.register("richie.chatterjee31@gmail.com", passw)
    yag = yagmail.SMTP("richie.chatterjee31@gmail.com", passw)
    image_folder = os.path.join(main_dir,'images')
    template_folder = os.path.join(main_dir,'templates')
    html_msg = [yagmail.inline(os.path.join(image_folder,"one_page_profile.png")),
    os.path.join(template_folder,"links.html"),
    main_dir + "/docs/Resume.pdf"]
    # Instantiate the Application object and execute required method.
    obj = Application(data)
    email = data['Email Address']
    """Send Email"""
    yag.send(email, obj.subject, html_msg)
    return render_template('user_form_response.html')

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
    print(data)
    Application(data).delete()
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
