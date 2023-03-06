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
        response = requests.get(f"{API_URL}promotion=True")
        return response.json()
    else:
        response = requests.get(f"{API_URL}promotion=False")
        return response.json()
