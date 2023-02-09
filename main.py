from datetime import datetime
from typing import Union
from fastapi import FastAPI, Query, Header, Request, Form
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse, HTMLResponse
# from psycopg2._psycopg import cursor
from pydantic import BaseModel
import psycopg2
import pymongo
from pymongo import MongoClient
import json

app = FastAPI()


# conn = psycopg2.connect(database="taxi", user="postgres", password="123", host="localhost", port="5432")
# conn.autocommit = True
# cursor = conn.cursor()
#
# client = MongoClient('localhost', 27017)
# db = client['test']
# series_collection = db['users']

@app.get("/")
def Index():
    with open("static/index.html") as file:
        content = file.read()
    return HTMLResponse(content=content, media_type="text/html")


# task 6
@app.post("/submit-form")
def submit_form(driver_iin: int = Form(),
                client_iin: int = Form(),
                location_start: str = Form(),
                location_finish: str = Form(),
                costs: int = Form(),
                time_start: str = Form(),
                time_finish: str = Form()):
    conn = psycopg2.connect(database="taxi", user="postgres", password="123", host="localhost", port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    # sql = "insert into route (taketime, finishtime ,location_start, location_finish, costs) values " \
    # "('" + time_start + "','" + time_finish + "', '" + location_start + "','" + location_finish + "'," + costs + ",)"
    cursor.execute(
        "insert into route (taketime, finishtime, locationstart, locationfinish, costs) values (%s, %s, %s, %s, %s)",
        (time_start, time_finish, location_start, location_finish, costs))
    cursor.execute("select * from route")
    result = cursor.fetchall()
    cursor.close()
    for r in result:
        print(r)


@app.get("/view-route")
def take_routes():
    conn = psycopg2.connect(database="taxi", user="postgres", password="123", host="localhost", port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("select * from route")
    result = cursor.fetchall()
    return result


@app.post("/update-route/{route_id}")
def change_finish(route_id: int, finishtime: str):
    conn = psycopg2.connect(database="taxi", user="postgres", password="123", host="localhost", port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"update route set finishtime = '{finishtime}' where id = '{route_id}'")
    cursor.execute("select * from route")
    result = cursor.fetchall()
    return result


@app.post("/get-route/{taketime}")
def get_route(taketime: str):
    conn = psycopg2.connect(database="taxi", user="postgres", password="123", host="localhost", port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT D.NAME, D.LASTNAME, R.COSTS, C.NAME, C.LASTNAME, "
                   f"R.LOCATIONFINISH, R.TAKETIME, R.FINISHTIME "
                   f"FROM ROUTE R "
                   f"INNER JOIN SCHEDULE S ON S.ID = R.IDSCHEDULE "
                   f"INNER JOIN CLIENT C ON C.ID = R.IDCLIENT "
                   f"INNER JOIN CAR ON CAR.ID = S.IDCAR "
                   f"INNER JOIN DRIVER D ON D.ID = S.IDDRIVER "
                   f"INNER JOIN BRAND B ON B.ID = CAR.IDBRAND "
                   f"INNER JOIN MODEL M ON M.ID = CAR.IDMODEL "
                   f"WHERE R.TAKETIME::text LIKE '%{taketime}%';")
    result = cursor.fetchall()
    return result


@app.post("/add-cashe")
def add_cashe_mongo(name: str, lastname: str, birthdate: str, phone: int, iin: int):
    client = MongoClient('localhost', 27017)
    db = client['test']
    series_collection = db['cashe']

    json_input = {
        "name": name,
        "lastname": lastname,
        "birthdate": birthdate,
        "phone": phone,
        "iin": iin
    }
    series_collection.insert_one(json_input)
    result = series_collection.find()
    return {
        "message": "user added to cashe"
    }


@app.post("/take-from-cashe")
def take_from_cashe(id):
    client = MongoClient('localhost', 27017)
    db = client['test']
    series_collection = db['cashe']

    # elements = input()
    # json2 = {"name":elements}
    # result = series_collection.(json.loads(elements)).inserted_id
    # result = series_collection.find(json.loads(elements))

    # json_input = {"_id": id}
    # result = series_collection.find({"_id": ObjectId("63e4ceb35777789a9d6ab8ba")})
    # return result
    # for r in result:
    #    print(type(r['name']))
