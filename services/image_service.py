import openai
import cloudinary
import cloudinary.uploader
import requests
import os

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

STYLE_SUFFIX = """
Style: cinematic landscape photography, National Geographic style,
dramatic natural lighting, ultra detailed, rich natural colors,
no text, no watermarks, no people unless tiny silhouette for scale.
"""

def generate_and_upload_image(image_prompt: str) -> str:
    full_prompt = f"{image_prompt}\n\n{STYLE_SUFFIX}"
    print(f"Generating image: {image_prompt[:80]}...")

    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=full_prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )

    temp_url = response.data[0].url
    image_bytes = requests.get(temp_url).content

    upload_result = cloudinary.uploader.upload(
        image_bytes,
        folder="stillforest-agent",
        resource_type="image"
    )

    permanent_url = upload_result["secure_url"]
    print(f"Image uploaded: {permanent_url}")
    return permanent_url

def generate_multiple_images(image_prompts: list) -> list:
    urls = []
    for i, prompt in enumerate(image_prompts):
        print(f"Generating image {i+1} of {len(image_prompts)}...")
        url = generate_and_upload_image(prompt)
        urls.append(url)
    return urls