import main
import sqlite3

def store(fileName, userID, taskName, dueDate):
    connection = sqlite3.connect(fileName)
    connection.execute("INSERT INTO Tasks VALUES (?,?,?)", (userID, taskName, dueDate))
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
