import sqlite3
import status

def store(fileName, userID, taskName, dueDate, ts):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Tasks WHERE timestamp=?", (ts,))
    possibleTask = cursor.fetchall()
    if len(possibleTask) == 0:
        connection.execute("INSERT INTO Tasks VALUES (?,?,?,?)", (userID, taskName, dueDate, ts))
        connection.commit()
        connection.close()
        return status.databaseStatus.STORED
    elif len(possibleTask) > 0:
        # Update
        connection.execute("UPDATE Tasks SET dueDate=(?) WHERE taskName=(?)", (dueDate, taskName))
        connection.commit()
        connection.close()
        return status.databaseStatus.UPDATED
    else:
        return status.databaseStatus.ERROR

def getTasks(fileName, userID):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Tasks WHERE userID=?", (userID,))
    taskData = cursor.fetchall()
    connection.close()
    return taskData

def getTasksByDate(fileName, date):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Tasks WHERE dueDate=?", (date,))
    taskData = cursor.fetchall()
    connection.close()
    return taskData

def remove(fileName, ts):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tasks WHERE timestamp=?", (ts,))
    connection.commit()
    connection.close()

    return status.databaseStatus.REMOVED

