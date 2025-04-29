from fastapi import FastAPI, Request
import paho.mqtt.publish as publish
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/github-webhook")
async def github_webhook(request: Request):
    data = await request.json()
    if data.get("ref") == "refs/heads/main":
        head_commit = data.get("head_commit", {})
        update_files = head_commit.get("added", []) 
        title = head_commit.get("message")
        queue_message = {
            "message": "New update available!",
            "title": title,
            "files": update_files
        }
        publish.single("update/notify", json.dumps(queue_message), hostname="localhost")
        print("MQTT message published: New update available!")
    return {"message": "Received"}
