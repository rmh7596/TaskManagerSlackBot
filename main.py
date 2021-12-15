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
    print(data)
    input = data.get('text')
    if input == "":
        client.chat_postMessage(channel='#development', text="Error: Task cannot be empty")
        return Response(), 200
    taskName = input
    view = taskCreationView.Task(taskName)
    client.chat_postMessage(channel='#development', **view.getMessage())
    return Response(), 200

@app.route('/handle-reaction', methods=['POST'])
def get_deadline():
    rawData = request.form
    parsedData = json.loads(rawData["payload"])

    try:
        action = parsedData['message']['blocks'][1]['elements'][0]['action_id'] # Date picker
    except IndexError:
        action = parsedData['message']['blocks'][0]['accessory']['action_id'] # Checkbox

    if (action == "datePicker"):
        storeTask(parsedData)
    elif action == "checkboxes-action":
        deleteTask(parsedData)
    return Response(), 200

def storeTask(parsedData):
    #Store timestamp
    selectedDate = parsedData['state']['values']['dateSelectionBox']['datePicker']['selected_date']
    task = parsedData['message']['blocks'][0]['text']['text'][16:] # Substringing to remove the "*Task Created: xxx *"
    userID = parsedData['user']['id']
    #Call store() passing taskName, seletedDate, userID
    database.store(os.environ['DATABASE'], userID, task, selectedDate)
    #Close database

def deleteTask(parsedData):
    # stuff
    print(parsedData)
    # Delete message when done
    return

@app.route('/my-tasks', methods=['POST'])
def get_tasks():
    rawData = request.form
    userID = rawData.get('user_id')
    tasks = database.getTasks(os.environ['DATABASE'], userID)

    client.chat_postMessage(channel="#development", text="Current number of tasks: " + str(len(tasks)))

    for i in range(len(tasks)):
        client.chat_postMessage(channel="#development", **taskDisplayView.displayTask(tasks[i]))
        time.sleep(2)

    return Response(), 200

# Send reminders

if __name__ == "__main__":
    app.run(debug=True)