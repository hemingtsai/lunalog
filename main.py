from contextlib import asynccontextmanager
import json
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import blog_manager
from auth import verify_github_signature
from typing import AsyncGenerator, List, Dict, Any

if not os.path.exists("config/config.json"):
    print("Configure file not found")
    exit(1)
config = json.loads(open("config/config.json", "r").read())


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global bm

    bm = blog_manager.BlogManager(config)
    bm.update_posts()

    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config["cors_allow_origin"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/posts/{post_id}")
def read_post(post_id: int) -> str:
    return bm.get_post(post_id)


@app.get("/posts_list")
def read_posts_list() -> List[Dict[str, Any]]:
    return bm.get_post_list()


@app.post("/webhook")
async def github_webhook(request: Request) -> Dict[str, str]:
    # 读取请求体
    body = await request.body()

    # 验证签名
    verify_github_signature(request, body)

    # 解析 JSON 数据
    payload: Dict[str, Any] = json.loads(body)  # type: ignore
    event_type = request.headers.get("X-GitHub-Event")

    # 处理不同的事件类型
    if event_type == "push":
        # 处理 push 事件
        print("Received push event")
        bm.update_posts()
    # 返回成功响应
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
