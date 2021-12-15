#Task name + checkbox to mark if it is complete
def displayTask(task):
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Task:* {task[1]} \t *Due Date:* {task[2]}"
                },
                "accessory": {
                    "type": "checkboxes",
                    "options": [
                        {
                        "text": {
							"type": "mrkdwn",
							"text": "Mark complete"
						},
                        "value": "value-0"
                        }
                    ],
                    "action_id": "checkbox-action"
                }
            }
        ]
    }