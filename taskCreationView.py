class Task:
    def __init__(self, taskName) -> None:
        self.taskName = taskName

    def formatTaskName(self):
        return {
            "type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Task Created*: {self.taskName}"
			}
    }

    def formatDateSelector(self):
        return {
			"type": "actions",
			"block_id": "dateSelectionBox",
			"elements": [
				{
					"type": "datepicker",
					"action_id": "datePicker",
					"placeholder": {
						"type": "plain_text",
						"text": "Select a due date"
					}
				}
			]
	}

    def formatInstruction(self):
        return {
            "type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "React with :white_check_mark: when completed!"
			}
	}

    def getMessage(self):
        return {
            'blocks' : [
                self.formatTaskName(),
                self.formatDateSelector(),
				self.formatInstruction()
        ]
    }