Инструкция

Код написан на python 3.9

Создайте виртуальное окружение и установите следующие библиотеки:

pip install requirements.txt

Необходимо запустить телеграм бота @Delivery_srok_bot

Оба скрипта работают независимо друг от друга.

Перед запуском нужно в начале файла ввести свои данные(см. комментарии)

Файл mypython-353411-2e8e872a5b0d.json необходимо положить в ту же папку, что и файлы.

Необходимо иметь базу данных PostgresSQL

Ссылка на Google sheets https://docs.google.com/spreadsheets/d/10CxbGyGH0C0-v2EVH0MOcjYGLdb0esAwzNo1L2ITTx8/edit#gid=0 

Первый скрипт каждую минуту запрашивает время изменения Google sheet, и если оно изменилось перезаписывает табдицу в базе данных.

Второй скрипт раз в сутки скачивает таблицу, и если находит в ней просроченные заказы отправляет сообщение в телеграм.

