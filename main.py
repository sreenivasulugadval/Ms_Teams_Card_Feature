from flask import Flask, render_template, request
from datetime import datetime
import Environment
from teams import send_request_to_teams, send_request_to_teams1
import ms_mail_sender1

app = Flask(__name__)

# Exist Users data: username with password in dict format
users_data = {
    "sreenu": "Sreenu@1998",
    "prasad": "Prasad@2000",
    "swetha": "Swetha@2000",
    "admin": "password"
}


servers = ["Server1", "Server2", 'meeza_server', 'jenkins_server', 'score_dev_ui', 'score_dev_api', 'score_uat_ui','score_uat_api']
all_servers = servers
server_details_dict = {
    'Server1': {'status': 'UP', 'config': 'linux', 'last_updated': 'None'},
    'Server2': {'status': 'DOWN', 'config': 'Window', 'last_updated': 'None'},
    'meeza_server': {'status': 'UP', 'config': 'Macos', 'last_updated': 'None'},
    'jenkins_server': {'status': 'DOWN', 'config': 'cent', 'last_': 'None'},
    'score_dev_ui': {'status': 'UP', 'config': 'linux', 'last_updated': 'None'},
    'score_dev_api': {'status': 'DOWN', 'config': 'Window', 'last_updated': 'None'},
    'score_uat_ui': {'status': 'UP', 'config': 'Macos', 'last_updated': 'None'},
    'score_uat_api': {'status': 'DOWN', 'config': 'cent', 'last_': 'None'}
}
three_dots_options = ["Edit", "Cancel"]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the submitted form data
        username = request.form.get('username')
        password = request.form.get('password')
        Environment.USER_NAME = username

        username_flag = False
        password_flag = False
        count = 0
        for key, value in users_data.items():
            if username == key:
                username_flag = True
                count = count + 1
                if password == value:
                    password_flag = True
                    break
                else:
                    username_flag = False

        # Perform authentication logic here, e.g. checking against a database

        # If authentication is successful, redirect to a dashboard page
        if username_flag and password_flag:
            return render_template('index2.html', servers=servers, server_details_dict=server_details_dict,
                                   all_servers=all_servers, options=three_dots_options, user=username)
        elif count >= 1 or username_flag and password_flag == False:
            return render_template('login.html', message="Incorrect password")
        else:
            return render_template('login.html', message="User not exist")

    except Exception as e:
        return render_template('login.html', message="An error occurred: " + str(e))

@app.route('/allservers')
def index1():
    return render_template('index2.html', servers=servers, server_details_dict=server_details_dict,all_servers= all_servers, selected_ser = " None", options=three_dots_options, link = "All servers", user=Environment.USER_NAME )

@app.route('/get_selected_server_details', methods=['POST'])
def get_selected_server_details():
    selected_server_List = [request.form['servers']]
    return render_template('index2.html', servers=selected_server_List, server_details_dict=server_details_dict,all_servers=all_servers, selected_ser = selected_server_List,options=three_dots_options,link = ("Selected " + str(selected_server_List[0])+ " details"), user=Environment.USER_NAME)

@app.route('/down-servers')
def down_servers():
    try:
        down_servers = []

        for server in servers:
            if server_details_dict[server]['status'] == "DOWN":
                down_servers.append(server)

        return render_template('index2.html', servers=down_servers, server_details_dict=server_details_dict,
                               all_servers=all_servers, link="Down Servers", user=Environment.USER_NAME)

    except Exception as e:
        return render_template('error.html', message="An error occurred: " + str(e))


@app.route('/up-servers')
def up_servers():
    try:
        up_servers = []
        for server in servers:
            if server_details_dict[server]['status'] != "DOWN":
                up_servers.append(server)
        return render_template('index2.html', servers=up_servers, server_details_dict=server_details_dict,
                               all_servers=all_servers, link="Up Servers", user=Environment.USER_NAME)

    except Exception as e:
        return render_template('error.html', message="An error occurred: " + str(e))


@app.route('/server_data_modify' , methods=['GET','POST'])
def server_data_modify():
    try:
        if request.method == 'POST':
            server_name = request.args.get('server')

            if server_details_dict[request.args.get('server')]['status'] == 'DOWN':
                purpose = 'UP'
            else:
                purpose = 'DOWN'

            send_request_to_teams(Environment.webhook_url, "Approval Pending from: ", purpose=purpose, servername=server_name)

            selc_serv = [request.args.get('server')]
            selected_server = server_details_dict[request.args.get('server')]
            server_status = selected_server['status']

            return render_template("edit.html", servers=selc_serv, server_details_dict=server_details_dict,
                                   all_servers=all_servers, status=server_status, Ack='waiting',
                                   link=(str(selc_serv[0]) + " details"), user=Environment.USER_NAME)

        selc_serv = [request.args.get('server')]
        selected_server = server_details_dict[request.args.get('server')]
        server_status = selected_server['status']

        return render_template("edit.html", servers=selc_serv, server_details_dict=server_details_dict,
                               all_servers=all_servers, status=server_status, link=(str(selc_serv[0]) + " details"), user=Environment.USER_NAME)

    except Exception as e:
        return render_template('error.html', message="An error occurred: " + str(e))

@app.route('/approve')
def approve_request1():
    try:
        servername = request.args.get('servername')

        server_details_dict[servername]['last_updated'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

        status = request.args.get('status')

        if status == 'DOWN':
            server_details_dict[servername]['status'] = 'DOWN'
        else:
            server_details_dict[servername]['status'] = 'UP'

        # Parse the request body
        subject = "Request Approved"
        body = {
            'contentType': 'HTML',
            'content': "Your request has been Approved."
        }
        mail_trigger_response = ms_mail_sender1.send_mail(subject, body)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        teams_response = send_request_to_teams1(Environment.webhook_url, "Aprroved  ", purpose=status, servername=servername)
        server_details_dict[servername]['last_updated'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

        message = 'Your Request is Approved successfully <br> <br> Note : Please check your email for confirmation and check acknowledgment in teams.'

        return render_template("edit.html", servers=[servername], server_details_dict=server_details_dict,
                               all_servers=all_servers, status=status, ack = 'approve', user=Environment.USER_NAME)
    except Exception as e:
        return f'<html><body><h3> Error : Unable to approve the Request by raghavendra <br> {str(e)} </h3></body></html>'


@app.route('/reject')
def reject_request():
    try:
        servername = request.args.get('servername')

        server_details_dict[servername]['last_updated'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

        status = request.args.get('status')

        if status == 'DOWN':
            server_details_dict[servername]['status'] = 'UP'
        else:
            server_details_dict[servername]['status'] = 'DOWN'

        # Parse the request body
        subject = "Request Rejected"
        body = {
            'contentType': 'HTML',
            'content': "Your request has been Rejected."
        }
        mail_trigger_response = ms_mail_sender1.send_mail(subject, body)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        teams_response = send_request_to_teams1(Environment.webhook_url, "Rejected  ", purpose=status, servername=servername)
        server_details_dict[servername]['last_updated'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

        message = 'Your Request is Approved successfully <br> <br> Note : Please check your email for confirmation and check acknowledgment in teams.'

        return render_template("edit.html", servers=[servername], server_details_dict=server_details_dict,
                               all_servers=all_servers, status=status, ack = 'reject', user=Environment.USER_NAME)

        #return render_template('edit.html', servername=servername, status=status , config = server_details_dict[servername]['config'],ack = 'approve')
    except Exception as e:
        return f'<html><body><h3> Error : Unable to approve the Request by raghavendra <br> {str(e)} </h3></body></html>'


if __name__ == '__main__':
    app.run(debug=True)
