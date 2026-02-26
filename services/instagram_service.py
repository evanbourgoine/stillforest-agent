import requests
import os
import time

INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
BASE_URL = "https://graph.facebook.com/v18.0"

def create_image_container(image_url: str, is_carousel_item: bool = False) -> str:
    data = {
        "image_url": image_url,
        "access_token": ACCESS_TOKEN
    }
    if is_carousel_item:
        data["is_carousel_item"] = "true"

    response = requests.post(
        f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media",
        data=data
    )

    result = response.json()
    if "error" in result:
        raise Exception(f"Image container failed: {result['error']}")

    return result["id"]

def post_to_instagram(image_url: str, caption: str) -> str:
    container_id = create_image_container(image_url)
    print(f"Media container created: {container_id}")
    time.sleep(5)

    publish_response = requests.post(
        f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }
    )

    publish_data = publish_response.json()
    if "error" in publish_data:
        raise Exception(f"Publishing failed: {publish_data['error']}")

    return publish_data["id"]

def post_carousel_to_instagram(image_urls: list, caption: str) -> str:
    # Step 1: Create individual image containers
    print(f"Creating {len(image_urls)} image containers...")
    container_ids = []
    for i, url in enumerate(image_urls):
        print(f"Creating container {i+1} of {len(image_urls)}...")
        container_id = create_image_container(url, is_carousel_item=True)
        container_ids.append(container_id)
        time.sleep(2)

    # Step 2: Create carousel container
    print("Creating carousel container...")
    carousel_response = requests.post(
        f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media",
        data={
            "media_type": "CAROUSEL",
            "children": ",".join(container_ids),
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }
    )

    carousel_data = carousel_response.json()
    if "error" in carousel_data:
        raise Exception(f"Carousel container failed: {carousel_data['error']}")

    carousel_id = carousel_data["id"]
    print(f"Carousel container created: {carousel_id}")
    time.sleep(5)

    # Step 3: Publish the carousel
    publish_response = requests.post(
        f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        data={
            "creation_id": carousel_id,
            "access_token": ACCESS_TOKEN
        }
    )

    publish_data = publish_response.json()
    if "error" in publish_data:
        raise Exception(f"Publishing failed: {publish_data['error']}")

    return publish_data["id"]