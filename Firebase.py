import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import mysql.connector

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin",
    database="smartclassroommonitor"
)
def getUser():
    mycursor = mydb.cursor()
    query = "SELECT * FROM user"
    mycursor.execute(query)
    results = []
    for row in mycursor.fetchall():
        results.append(row[2])
    mycursor.close()

    return results

def send_push_notification(token, title, body):
    message = {
        'title': title,
        'body': body
    }
    try:
        response = messaging.send(messaging.Message(
            token=token,
            notification=messaging.Notification(
                title=message['title'],
                body=message['body']
            )
        ))
        print('Notification sent successfully:', response)
    except messaging.UnregisteredError:
        # Handle the case when the token is unregistered
        # Remove the invalid token from your server or mark it as inactive
        print('Unregistered token:', token)
    except Exception as e:
        # Handle other errors
        print('Error sending notification:', str(e))


# Replace the tokens, title, and body with your desired values
title = "Notification Title"
body = "Notification Body"

for token in getUser():
    print(token)
    send_push_notification(token, title, body)
