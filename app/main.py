from time import sleep

import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routes import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='osho0083', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connected Successfully")
        break
    except Exception as error:
        print("Connecting To Database Failed")
        print("Error: ", error)
        sleep(2)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "welcome to my first api"}
