from datetime import datetime
from typing import Union
from fastapi import FastAPI, Query, Header, Request, Form
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse, HTMLResponse
from psycopg2._psycopg import cursor
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


@app.post("/take-route/{route_id}")
def change_finish(route_id: int, finishtime: str):
    conn = psycopg2.connect(database="taxi", user="postgres", password="123", host="localhost", port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"update route set finishtime = '{finishtime}' where id = '{route_id}'")
    cursor.execute("select * from route")
    result = cursor.fetchall()
    return result


