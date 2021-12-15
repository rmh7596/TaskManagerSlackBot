#Task name + checkbox to mark if it is complete
def displayTask(task):
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Task:* {task[1]} \t *Due Date:* {task[2]}"
                }
            }
        ]
    }