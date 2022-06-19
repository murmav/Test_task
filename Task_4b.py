# Введите свой User Id из Telegram
chat_id = "695239657"

from datetime import datetime
import pandas as pd
import requests
import time
from google.oauth2 import service_account
import gspread


# Переменные, не изменяющиеся при работе скрипта
SCOPES = ['https://www.googleapis.com/auth/drive'] # позволяет просматривать, редактировать, удалять или создавать файлы на Google Диске
SERVICE_ACCOUNT_FILE = 'mypython-353411-2e8e872a5b0d.json' #путь к файлу с ключами сервисного аккаунта
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES) #учетные данные
client = gspread.authorize(credentials)
sheet = client.open("copy_test").sheet1  # Открывает google sheets


def get_table(sheet): # скачивание таблицы
    data = sheet.get_all_records()
    headers = data[0]
    df = pd.DataFrame(data,columns=headers)
    return df


def send_msg(text, chat_id): # отправка сообщения в телеграм
    token = "5553320004:AAGNEV9mh2_RnqKfY3WrSutms2ONWfYEdvM"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    requests.get(url_req)




while True:
    dt = datetime.now() # получаем сегодняшнюю дату
    df = get_table(sheet)  # скачиваем таблицу
    df['срок поставки'] = pd.to_datetime(df['срок поставки'], format="%d.%m.%Y")  #фильтруем таблицу по просроченной дате
    Bot_write = ", ".join(str(e) for e in list(df[df['срок поставки']<dt]['заказ №']))  #записываем номера просроченных заказов
    if Bot_write != '': # проверяем есть ли просроченные заказы
        send_msg(f'Эти заказы просрочены {Bot_write}', chat_id)  # отправляем сообщение
    time.sleep(86400)  # ждем сутки






