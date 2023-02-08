import psycopg2
import pymongo
from pymongo import MongoClient
import json

conn = psycopg2.connect(database="taxi", user="postgres", password="123", host="localhost", port="5432")
conn.autocommit = True
cursor = conn.cursor()

client = MongoClient('localhost', 27017)
db = client['test']
series_collection = db['users']


def first_task():
    name = input("Введите имя: ")
    birthdate = input("Введите дату рождения: ")
    lastname = input("Введите фамилию: ")
    phone = input("Введите телефон: ")
    iin = input("Введите ИИН: ")
    sql = "insert into client (name, lastname, birthdate, phone, iin) values " \
          "('" + name + "','" + lastname + "','" + birthdate + "', '" + phone + "','" + iin + "')"
    cursor.execute(sql)
    cursor.execute("select * from client")
    result = cursor.fetchall()
    print(result)


def second_task():
    name = input("Введите имя: ")
    birthdate = input("Введите дату рождения: ")
    lastname = input("Введите фамилию: ")
    phone = input("Введите телефон: ")
    iin = input("Введите ИИН: ")
    json_input = {
        "name": name,
        "lastname": lastname,
        "birthdate": birthdate,
        "phone": phone,
        "iin": iin
    }
    series_collection.insert_one(json_input)
    result = series_collection.find()
    for r in result:
        print(r)


# def third_task():

def forth_task():
    name = input("Введите имя: ")
    json_input = {
        "name": name
    }
    result = series_collection.find(json_input)
    for r in result:
        print(r)


def fifth_task():
    name = input("Введите имя: ")
    sql = "SELECT " \
          "R.id, " \
          "D.NAME AS Driver_name, " \
          "D.LASTNAME AS Driver_lastname, " \
          "C.NAME AS Client_name, " \
          "C.LASTNAME AS Client_name, " \
          "R.Locationstart, " \
          "R.LOCATIONFINISH, " \
          "R.COSTS FROM ROUTE R " \
          "INNER JOIN SCHEDULE S ON S.ID = R.IDSCHEDULE " \
          "INNER JOIN CLIENT C ON C.ID = R.IDCLIENT " \
          "INNER JOIN DRIVER D ON D.ID = S.IDDRIVER " \
          "Where c.name = '"+name+"' "

    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)

fifth_task()