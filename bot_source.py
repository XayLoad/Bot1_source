from random import randint
from requests import *
import json
import vk
import datetime
import mysql.connector

# Полезные ссылки: vk.com/dev, vk.com/dev/methods.


date = datetime.date.today()
print(date)
time = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
print(time)

cnx = mysql.connector.connect(user='mysql', password='mysql',
                              host='localhost',
                              database='bot_test')

cursor = cnx.cursor()

VK_API_ACCESS_TOKEN = '****'
VK_API_VERSION = '5.101'
GROUP_ID = 187433456

session = vk.Session(access_token=VK_API_ACCESS_TOKEN)
api = vk.API(session, v=VK_API_VERSION)


# функция для создания клавиатуры
def get_button(label, color, payload):
    return {
        "action": {
            "type": "text",
            "payload": payload,
            "label": label
        },
        "color": color
    }


# клавиатура
keyboard = {
    "one_time": False,
    "buttons": [
        [get_button("Test1", "primary", {"command": "t1"})],
        [get_button("Test2", "secondary", {"command": "t2"})],
        [get_button("Test3", "negative", {"command": "t3"})],
        [get_button("Test4", "positive", {"command": "t4"})]
    ]
}


keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

# Первый запрос к LongPoll: получаем server и key
longPoll = api.groups.getLongPollServer(group_id=GROUP_ID)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']

# Последующие запросы: меняется только ts
while True:
    longPoll = post('%s' % server, data={'act': 'a_check',
                                         'key': key,
                                         'ts': ts,
                                         'wait': 25}).json()
    if longPoll['updates'] and len(longPoll['updates']) != 0:
        for update in longPoll['updates']:
            text = update['object']['text']
            ids = update['object']['from_id']
            if update['object']['text'] == 'клава' or update['object']['text'] == 'Клава':
                api.messages.send(user_id=update['object']['from_id'],
                                  random_id=randint(-2147483648, 2147483647),
                                  message='Держи',
                                  keyboard=keyboard)
            elif update['object']['text'] == '2':
                api.messages.send(user_id=update['object']['from_id'],
                                  random_id=randint(-2147483648, 2147483647),
                                  message='1',
                                  keyboard=keyboard)
            if update['type'] == 'message_new' and update['object']['peer_id'] >= 2000000001:
                print(update)
                cursor.execute('''INSERT INTO message (DATE, time, id, MSG)
                               VALUES 
                               (%s, %s, %s, %s)''', (date, time, ids, text))
            if update['object']['text'] == 'Одмен Панель' and update['object']['from_id'] == "119640502":
                api.messages.send(peer_id=update['object']['peer_id'],
                                  random_id=randint(-2147483648, 2147483647),
                                  message='Админ панель:',
                                  keyboard=keyboard)
            ts = longPoll['ts']
            cnx.commit()
            try:
                if json.loads(update['object']['payload'])['command'] == 'start':
                    api.messages.send(user_id=update['object']['from_id'],
                                      random_id=randint(-2147483648, 2147483647),
                                      message='2',
                                      keyboard=keyboard)
                elif json.loads(update['object']['payload'])['command'] == 't1':
                    api.messages.send(user_id=update['object']['from_id'],
                                      random_id=randint(-2147483648, 2147483647),
                                      message='Test1',
                                      keyboard=keyboard)
                elif json.loads(update['object']['payload'])['command'] == 't2':
                    api.messages.send(user_id=update['object']['from_id'],
                                      random_id=randint(-2147483648, 2147483647),
                                      message='Test2',
                                      keyboard=keyboard)
                elif json.loads(update['object']['payload'])['command'] == 't3':
                    api.messages.send(user_id=update['object']['from_id'],
                                      random_id=randint(-2147483648, 2147483647),
                                      message='Test3',
                                      keyboard=keyboard)
                elif json.loads(update['object']['payload'])['command'] == 't4':
                    api.messages.send(user_id=update['object']['from_id'],
                                      random_id=randint(-2147483648, 2147483647),
                                      message='Test4',
                                      keyboard=keyboard)
                ts = longPoll['ts']

                cnx.commit()

            except KeyError:
                print(update)
