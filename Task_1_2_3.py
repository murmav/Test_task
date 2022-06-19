# Введите данные о базе данных в таком формате user:password@hostname/database_name
data_of_db = 'postgres:mashina@localhost:5432/postgres'

from google.oauth2 import service_account
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import gspread
import pandas as pd
import time
import urllib.request
from xml.dom import minidom


def get_modified_time(service, name_of_sheets):   # функция получения даты последнего изменения гугл листа
    results = service.files().list(pageSize=10,
                               fields="nextPageToken, files(name, modifiedTime)").execute() #список файлов и папок, к которым имеет доступ сервиc
    for i in results['files']:
        if i['name'] == name_of_sheets:
            mt = i['modifiedTime']
    return mt


def get_table(sheet): # скачивание таблицы
    data = sheet.get_all_records() 
    headers = data[0]
    df = pd.DataFrame(data,columns=headers)
    return df


def change_rubles(df): # получение столбца стоимости в рублях
    price_rubles = list()
    for _, row in df.iterrows():
        data_format = row['срок поставки'].replace('.','/')
        url =f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={data_format}"
        webFile = urllib.request.urlopen(url)

        data = webFile.read()
        dom = minidom.parseString(data) #создаем объект дом
        dom.normalize() # производим нормализацию объекта для ускорения работы
        indicator = 0  # индикатор для выхода из цикла
        elements = dom.getElementsByTagName('Valute') #получаем все узлы в корневом каталоге с тегом Valute

        for node in elements: 
            for child in node.childNodes: # перебираем дочерние ноды
                if child.tagName == "CharCode" and child.firstChild.data == "USD":
                    indicator = 1
                if child.tagName == "Value" and indicator == 1:
                    value = float(child.firstChild.data.replace(',','.'))
                    indicator = 2
            if indicator == 2:
                break
        price_rubles.append(row['стоимость,$']*value)
    return price_rubles


def db_create(df): # запись таблицы в базу даннных
    sql = str('DROP TABLE IF EXISTS test')
    engine.execute(sql)
    df.to_sql('test', engine,index=False) 


# Переменные, не изменяющиеся при работе скрипта
SCOPES = ['https://www.googleapis.com/auth/drive'] # позволяет просматривать, редактировать, удалять или создавать файлы на Google Диске
SERVICE_ACCOUNT_FILE = 'mypython-353411-2e8e872a5b0d.json' #путь к файлу с ключами сервисного аккаунта
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES) #учетные данные
service = build('drive', 'v3', credentials=credentials) 
client = gspread.authorize(credentials)
sheet = client.open("copy_test").sheet1  # Открывает google sheets
engine = create_engine(f'postgresql://{data_of_db}')
modified_time = '2000-01-00T17:08:17.761Z' # Неправильное время последнего изменения, чтобы при включении скрипт сразу записал таблицу в базу данных


while True:
    if get_modified_time(service, 'copy_test') != modified_time: # сравниваем даты изменения, чтобы понять нужна ли перезапись таблицы
        modified_time = get_modified_time(service, 'copy_test')
        df = get_table(sheet)  # скачиваем таблицу
        price_rubles = change_rubles(df)  # создаем столбец стоимости в рублях
        df = df.join(pd.DataFrame(price_rubles))  # добавляем столбец стоимости в рублях в таблицу
        db_create(df) # записываем таблицу в базу данных
    time.sleep(60)









