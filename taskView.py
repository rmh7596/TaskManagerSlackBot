class Task:
    DIVIDER = {'type' : 'divider'}
    def __init__(self, taskName) -> None:
        self.taskName = taskName

    def formatTask(self):
        return {
            'type' : 'section',
            'text' : {
                'type' : 'mrkdwn',
                'text' : (
                    'Task name: ' + self.taskName + ' created'
                )
            }
        }

    def getMessage(self):
        return {
            'blocks' : [
                self.formatTask(),
                self.DIVIDER
            ]
        }