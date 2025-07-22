import hashlib
import hmac
import json
from fastapi import Request, HTTPException

github_webhook_secret = json.loads(
    open("config.json", "r", encoding="utf-8").read()
)["github_webhook_secret"]

def verify_github_signature(request: Request, body: bytes) -> None:
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header:
        raise HTTPException(
            status_code=401, detail="No signature header")

    sha_name, signature = signature_header.split("=")
    if sha_name != "sha256":
        raise HTTPException(
            status_code=401, detail="Invalid signature algorithm")

    mac = hmac.new(github_webhook_secret.encode(),
                   msg=body, digestmod=hashlib.sha256)
    expected_signature = mac.hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=401, detail="Invalid signature")