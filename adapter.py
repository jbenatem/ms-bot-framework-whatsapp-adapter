from flask import Flask, request, abort
import requests
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/whatsapp/api/send", methods=['POST'])
def send_message_to_whatsapp():
    data = request.get_json()
    if (data != None):
        senderId = data.get("senderId")
        token = data.get("token")
        message = data.get("message")
    else: 
        abort(400)
    
    url = "https://graph.facebook.com/v18.0/" + senderId + "/messages"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    payload = json.dumps(message)
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.text
    elif response.status_code <= 499 and response.status_code >= 400: 
        return "<h2>Error por parte del cliente</h2>"
    elif response.status_code <= 599 and response.status_code >= 500: 
        return "<h2>Error por parte del servidor</h2>"
    else: 
        return "<h2>Error desconocido</h2>"