import json
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


API_URL = 'http://api.nookaton.ru/?'
API_KEY = 'key=tw8pyxRrPc5J62aVywJ78SvhnuhWGCwc'
API_KEY = API_KEY + '&'
API_URL = API_URL + API_KEY

async def CategoryMenu(obj):
    text = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
    elements = json.loads(text)
    menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for element in elements:
        menu.add(KeyboardButton(str(element).replace("[", "").replace("]", "").replace("'", "")))
    return menu

async def GetRequest():
    response = requests.get(f"{API_URL}categories=True")
    return response.json()

async def promotion(state):
    if state == True:
        requests.get(f"{API_URL}promotion=True")
    else:
        requests.get(f"{API_URL}promotion=False")

async def inapp_notification(title, message):
    if len(title) == 0:
        return 'Title error'
    if len(message) == 0:
        return 'Message error'
    requests.get(f'{API_URL}notification=True&title={title}&message={message}')