import json
import os
from datetime import datetime

REPLY_LOG_FILE = "data/reply_log.json"

def load_reply_log() -> dict:
    if not os.path.exists(REPLY_LOG_FILE):
        return {"replied_comment_ids": [], "replies": []}
    with open(REPLY_LOG_FILE, "r") as f:
        return json.load(f)

def has_been_replied_to(comment_id: str) -> bool:
    log = load_reply_log()
    return comment_id in log["replied_comment_ids"]

def save_reply(comment_id: str, comment_text: str, 
               reply_text: str, post_id: str, username: str):
    log = load_reply_log()
    
    log["replied_comment_ids"].append(comment_id)
    log["replies"].append({
        "date": datetime.now().isoformat(),
        "post_id": post_id,
        "username": username,
        "comment_id": comment_id,
        "comment_text": comment_text,
        "reply_text": reply_text
    })

    os.makedirs("data", exist_ok=True)
    with open(REPLY_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)
    
    print(f"Reply logged for comment by @{username}")