from flask import Flask
from common import UsersAvgManager

app = Flask(__name__)

SIMPLE_HTML = '''
                <!doctype html>
                <title>Avg Results</title>
                <h1>{title}</h1>
                <h2>{result}</h2>
                '''


@app.route('/average')
def uploaded_file():
    return SIMPLE_HTML.format(title = "All users average", result = UsersAvgManager.get_total_avg())


@app.route('/average/<slack_username>')
def uploaded_file(slack_username):
    return SIMPLE_HTML.format(title = "User average is", result = UsersAvgManager.get_user_avg(slack_username))
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)