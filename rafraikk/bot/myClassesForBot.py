import requests
import json
import asyncio

class MyBot:
    def __init__(self, TOKEN):
        self.info = "Test"
        self.TOKEN = TOKEN
        self.urlShort = f"https://api.telegram.org/bot{self.TOKEN}/"
        self.commandsBot = []
        self.checkBotCommands()

    def checkBotCommands(self):
        url = self.urlShort + 'getMyCommands'
        response = requests.get(url=url).json()
        if len(response['result']) == 0:
            self.info = "No Commands"
            self.creatCommands()
        else:
            self.getCommandsArray = response['result']
            for command in response['result']:
                self.commandsBot.append(command["command"])
            self.info = response['result'][-1]["command"]

    def analyseRequest(self, func):
        def wrapperRequest(data):
            if 'entities' in data['message'].keys():
                if data['message']['entities'][-1]["type"] == "bot_command":
                    strMes = self.makeCommandAnswer(data['message']["text"])
            else:
                strMes = f"'{data['message']['text']}' - it's not command"
            func(data, strMes)

        return wrapperRequest

    def makeCommandAnswer(self, command):
        analyze = command.split(" ")
        if len(analyze) == 1:
            match command:
                case "/start":
                    strMes = "Привет! Этот бот может выполнять некоторые команды."
                case "/contact":
                    strMes = "В дальнейшем будет команда /Контакты"
                case "/weather":
                    strMes = "Что бы получить погоду, введите следующее:\n/weather 'название города'"
                case _:
                    strMes = "Пока работает только команда /weather."
            return strMes
        else:
            if analyze[0] == "/weather":
                strMes = f"Температура в {analyze[1]}: "
                strMes += str(self.getWeather(analyze[1]))
            else: strMes = "Пока работает только команда /weather."
            return strMes

    def getWeather(self, city):
        city = city
        urlWeather = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': 'a876f8f80d90c1ac61e3f0613b7d495a',
            'units': 'metric',
            'lang': 'ru'
        }

        response = requests.post(url=urlWeather, params=params).json()
        return response['main']['temp']

    def creatCommands(self):
        url = self.urlShort + 'setMyCommands'
        commandsBot = [{'command': 'start', 'description': "start working"}]
        commandsBot = json.dumps(commandsBot)
        param_commands = {
            'commands': commandsBot
        }
        response = requests.get(url=url, params = param_commands).json()

    def addCommand(self, command):
        url = self.urlShort + 'setMyCommands'
        commandsBot = {'command': command, 'description': f"{command} command"}
        self.getCommandsArray.append(commandsBot)
        commandsBotAlljs = json.dumps(self.getCommandsArray)
        param_commands = {
            'commands': commandsBotAlljs
        }
        response = requests.get(url=url, params = param_commands).json()

    def setMenuBot(self):
        url = self.urlShort + 'setChatMenuButton'
        menu_button_options = {
                 'type': 'default'
        }
        menu_button_options = json.dumps(menu_button_options)
        params = {
             'menu_button': menu_button_options
        }
        response = requests.get(url=url, params=params).json()


