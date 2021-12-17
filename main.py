from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import database
import status
import json
import taskCreationView
import errors
import logging as log

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)
app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

@app.route('/create-task', methods=['POST'])
def create_task():
    log.info("task created")
    data       = request.form
    log.debug(data)
    input      = data.get('text')
    channel_id = data.get('channel_id')

    if input == "":
        client.chat_postMessage(channel=channel_id, text="Error: Task cannot be empty")
        return Response(), 200
    
    taskName = input
    view     = taskCreationView.Task(taskName)
    client.chat_postMessage(channel=channel_id, **view.getMessage())
    return Response(), 200

@app.route('/submit-deadline', methods=['POST'])
def get_deadline():
    log.info("deadline submitted")
    rawData      = request.form
    parsedData   = json.loads(rawData["payload"])
    log.info(f"parsed data {parsedData}", parsedData)
    selectedDate = parsedData['state']['values']['dateSelectionBox']['datePicker']['selected_date']
    task         = parsedData['message']['blocks'][0]['text']['text'][16:] # Substringing to remove the "*Task Created: xxx *"
    userID       = parsedData['user']['id']
    ts           = parsedData['container']['message_ts']
    channel_id   = parsedData['container']['channel_id']
    link         = client.chat_getPermalink(channel=channel_id, message_ts=ts).get('permalink')

    if database.store(os.environ['DATABASE'], userID, task, selectedDate, ts, channel_id, link) == status.databaseStatus.ERROR:
        log.error("Unable to update database entry")
        raise errors.databaseStorageError

    return Response(), 200

@slack_event_adapter.on('reaction_added')
def reactionAdded(payload):
    log.debug("reaction added")
    log.info(f"payload: {payload}", payload)
    event             = payload.get('event', {})
    channel_id        = event.get('item', {}).get('channel')
    message_timestamp = event.get('item', {}).get('ts')

    if event.get('reaction') == 'white_check_mark':
        log.debug("Removing task")
        database.remove(os.environ['DATABASE'], message_timestamp)
        client.chat_delete(channel=channel_id, ts=message_timestamp)

    if event.get('reaction') == '+1':
        log.debug("Removing reminder")
        client.chat_delete(channel=channel_id, ts=message_timestamp)

scheduler = BackgroundScheduler()
@scheduler.scheduled_job(IntervalTrigger(days=1))
def reminders():
    today_tasks = database.getTasksByDate(os.environ['DATABASE'], date.today())
    log.info(f"Todays reminder to send out: {today_tasks}", today_tasks)
    for task in today_tasks:
        user_id   = task[0]
        task_name = task[1]
        user_str  = "@" + user_id
        link      = task[5]

        client.chat_postMessage(channel=user_str, text="*Reminder*: " + task_name + " is due today. Clear reminder using :+1:. Clear task <" + link + "|here>")


if __name__ == "__main__":
    log.basicConfig(filename=os.environ['LOGGING'], encoding='utf-8', level=log.DEBUG)
    log.info("Starting scheduler")
    scheduler.start()
    app.run(debug=True, use_reloader=False)