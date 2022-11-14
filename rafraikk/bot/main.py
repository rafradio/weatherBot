from flask import Flask, render_template, redirect, url_for
from flask_sslify import SSLify
from flask import jsonify
from flask import request
import requests
import json
import asyncio
import rafraikk.bot.myClassesForBot as myClassesForBot

app = Flask(__name__)
sslify = SSLify(app)


TOKEN = ""
with open('token.txt', 'r') as token:
    TOKEN = token.read()

myBot = myClassesForBot.MyBot(TOKEN)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
urlShort = f"https://api.telegram.org/bot{TOKEN}/"
name = "Raf"
commands = []

@myBot.analyseRequest
def sendMessage(data, srtMes):
    chat_id = int(data['message']['chat']['id'])
    params = {
            'chat_id': chat_id,
            'text': srtMes
    }
    response = requests.post(url=url, params=params).json()


@app.route('/rafraikkBot/', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        r = request.get_json()
#        srtMes = "Bye Bye\n\nok"

        sendMessage(r)
        with open('answer2.json', 'w') as f1:
            json.dump(r, f1, indent=2)
        textStr = r["message"]["text"]
    else: textStr = "hello"

    with open('answer.txt', 'w') as f:
        f.write(request.method)

    return 'hello world from %s' % name

@app.route('/', methods=['POST', 'GET'])
def index():
    user = 'Raf'
    if request.method == 'POST':
        command = request.form['fname']
        if command not in myBot.commandsBot:
            commands.append(command)
            myBot.addCommand(command)
    else: command = ""

#    myBot.checkBotCommands()
    with open('testPy.txt', 'w') as f:
        f.write(myBot.info)

#    myBot.setMenuBot()

    return render_template('hello.html', insertName=commands)

def main():
    pass


if __name__ == '__main__':
    # main()
    app.debug = True
    app.run()