from datetime import datetime 
import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import database
import taskView

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

@app.route('/create-task', methods=['POST'])
def create_task():
    data = request.form
    #database.connectToDatabase()
    input = data.get('text')
    args = input.split(',')
    taskName = args[0]
    view = taskView.Task(taskName)
    client.chat_postMessage(channel='#development', **view.getMessage())
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    print("Current Time =", current_time)
    return Response(), 200

# /my-tasks
    # is it done?

# Send reminders

if __name__ == "__main__":
    app.run(debug=True)