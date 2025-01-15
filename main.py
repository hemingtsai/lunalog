from contextlib import asynccontextmanager

from fastapi import FastAPI

import blog_manager

blog_manager_c: blog_manager.BlogManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bm

    bm = blog_manager.BlogManager()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/posts/{post_id}")
def read_post(post_id: int):
    return bm.get_post(post_id)


@app.get("/posts_list")
def read_posts_list():
    return bm.get_post_list()
