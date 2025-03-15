from contextlib import asynccontextmanager
import json
import os
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import blog_manager
import hashlib
import hmac

if not os.path.exists("config/config.json"):
    print("Configure file not found")
    exit(1)
config = json.loads(open("config/config.json", "r").read())


@asynccontextmanager
async def lifespan(app: FastAPI):
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
def read_post(post_id: int):
    return bm.get_post(post_id)


@app.get("/posts_list")
def read_posts_list():
    return bm.get_post_list()


def verify_github_signature(request: Request, body: bytes):
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header:
        raise HTTPException(
            status_code=401, detail="No signature header")

    sha_name, signature = signature_header.split("=")
    if sha_name != "sha256":
        raise HTTPException(
            status_code=401, detail="Invalid signature algorithm")

    mac = hmac.new(config["github_webhook_secret"].encode(),
                   msg=body, digestmod=hashlib.sha256)
    expected_signature = mac.hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=401, detail="Invalid signature")


@app.post("/webhook")
async def github_webhook(request: Request):
    # 读取请求体
    body = await request.body()

    # 验证签名
    verify_github_signature(request, body)

    # 解析 JSON 数据
    payload = json.loads(body)
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
