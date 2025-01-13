from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import database_control

@asynccontextmanager
async def lifespan(app:FastAPI):
    database_control.init_database()

    yield
    
    database_control.close_database()

app = FastAPI(lifespan=lifespan)

@app.get("/posts/{post_id}")
def read_post(post_id:int):
    return database_control.get_post(post_id)
        