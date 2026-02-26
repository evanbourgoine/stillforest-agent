import requests
import os

INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
BASE_URL = "https://graph.facebook.com/v18.0"

def get_recent_posts(limit: int = 5) -> list:
    response = requests.get(
        f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media",
        params={
            "fields": "id,caption,timestamp",
            "limit": limit,
            "access_token": ACCESS_TOKEN
        }
    )

    data = response.json()

    if "error" in data:
        raise Exception(f"Failed to fetch posts: {data['error']}")

    return data.get("data", [])

def get_comments_on_post(post_id: str) -> list:
    response = requests.get(
        f"{BASE_URL}/{post_id}/comments",
        params={
            "fields": "id,text,timestamp,username",
            "access_token": ACCESS_TOKEN
        }
    )

    data = response.json()

    if "error" in data:
        raise Exception(f"Failed to fetch comments: {data['error']}")

    return data.get("data", [])

def reply_to_comment(comment_id: str, reply_text: str) -> str:
    response = requests.post(
        f"{BASE_URL}/{comment_id}/replies",
        data={
            "message": reply_text,
            "access_token": ACCESS_TOKEN
        }
    )

    data = response.json()

    if "error" in data:
        raise Exception(f"Failed to post reply: {data['error']}")

    return data["id"]