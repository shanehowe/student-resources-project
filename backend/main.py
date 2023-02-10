from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_router import user_router
from routes.login_router import login_router
from routes.resource_router import resource_router
from routes.challenges_router import challlenge_router
from dotenv import load_dotenv
from database.database import database
import os

load_dotenv(".env")

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATA_BASE")
DEV_ORIGIN = os.getenv("DEV_ORIGIN")
origins = ["https://resource-centre.herokuapp.com", DEV_ORIGIN]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(challlenge_router)
app.include_router(user_router)
app.include_router(login_router)
app.include_router(resource_router)



@app.on_event("startup")
def connect_to_db():
    database.connect(MONGO_URI, DATABASE_NAME)


@app.on_event("shutdown")
def close_client():
    database.client.close()