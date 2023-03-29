FoodAdviserBot - проект телеграм бота, который высылает перечень продуктов, исходя из выбранной диеты (список которых находиться в БД).

Инструкция по установке, настройке и запуску проекта:

- скачайте все файлы данного проекта
- поместите их в одну папку
- создайте бота в https://web.telegram.org/z/#93372553
- установите postgresql
- создайте учетную запись в postgresql
- создайте базу данных в postgresql
- в файле .env укажите: 
DATABASE_PORT, 
POSTGRES_PASSWORD, 
POSTGRES_USER, 
POSTGRES_DB, 
POSTGRES_HOST, 
POSTGRES_HOSTNAME,
URL = 'https://api.telegram.org/bot',
BOT_TOKEN.


- запустите файл main `python main.py`
- остановите работу программы
- в postgresql в таблицу diets добавьте диеты
- в postgresql в таблицу products добавьте продукты и их каллорийность на 100 грамм
- в postgresql в таблицу diet_details вставьте id диеты в колонку diet и id продуктов, относящихся к конкретной диете, в колонку product
- снова запустите файл main
- в чате с ботом напишите /start


![img.png](img.png)
![img_1.png](img_1.png)
