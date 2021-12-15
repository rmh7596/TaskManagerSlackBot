from asyncio.windows_events import NULL
from typing import Text
import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import database
import time
import json
import taskCreationView
import taskDisplayView

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

@app.route('/create-task', methods=['POST'])
def create_task():
    data = request.form
    input = data.get('text')
    if input == "":
        client.chat_postMessage(channel='#development', text="Error: Task cannot be empty")
        return Response(), 200
    taskName = input
    view = taskCreationView.Task(taskName)
    client.chat_postMessage(channel='#development', **view.getMessage())
    return Response(), 200

@app.route('/submit-deadline', methods=['POST'])
def get_deadline():
    rawData = request.form
    parsedData = json.loads(rawData["payload"])
    selectedDate = parsedData['state']['values']['dateSelectionBox']['datePicker']['selected_date']
    task = parsedData['message']['blocks'][0]['text']['text'][16:] # Substringing to remove the "*Task Created: xxx *"
    userID = parsedData['user']['id']
    ts = parsedData['container']['message_ts']
    #Call store() passing taskName, seletedDate, userID
    database.store(os.environ['DATABASE'], userID, task, selectedDate, ts)
    #Close database
    return Response(), 200

@app.route('/my-tasks', methods=['POST'])
def get_tasks():
    rawData = request.form
    userID = rawData.get('user_id')
    tasks = database.getTasks(os.environ['DATABASE'], userID)

    for i in range(len(tasks)):
        client.chat_postMessage(channel="#development", **taskDisplayView.displayTask(tasks[i]))
        time.sleep(2)

    client.chat_postMessage(channel='#development', text="React with :white_check_mark: when completed")
    return Response(), 200

@slack_event_adapter.on('reaction_added')
def reactionAdded(payload):
    event = payload.get('event', {})
    channel_id = event.get('item', {}).get('channel')
    timestamp = event.get('item', {}).get('ts')
    database.remove(os.environ['DATABASE'], timestamp)
    client.chat_delete(channel=channel_id, ts=timestamp)
# Send reminders

if __name__ == "__main__":
    app.run(debug=True)