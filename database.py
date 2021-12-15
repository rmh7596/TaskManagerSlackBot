import main
import sqlite3

def store(fileName, userID, taskName, dueDate, ts):
    connection = sqlite3.connect(fileName)
    connection.execute("INSERT INTO Tasks VALUES (?,?,?,?)", (userID, taskName, dueDate, ts))
    connection.commit()
    connection.close()
    return

def getTasks(fileName, userID):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Tasks WHERE userID=?", (userID,))
    taskData = cursor.fetchall()
    connection.close()
    return taskData

def remove(fileName, ts):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tasks WHERE timestamp=?", (ts,))
    connection.commit()
    connection.close()
# Remove from db when task is marked as complete
# Add reaction handling
# Add reminders through direct messaging

