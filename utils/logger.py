import json
import os
from datetime import datetime

LOG_FILE = "data/post_log.json"

def load_history() -> list:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def get_past_topics() -> list:
    history = load_history()
    return [entry["topic"] for entry in history]

def save_post(topic: str, content_pillar: str, caption: str,
              image_url: str, instagram_post_id: str):
    history = load_history()
    history.append({
        "date": datetime.now().isoformat(),
        "topic": topic,
        "content_pillar": content_pillar,
        "caption": caption,
        "image_url": image_url,
        "instagram_post_id": instagram_post_id
    })
    os.makedirs("data", exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)
    print(f"Post logged successfully.")