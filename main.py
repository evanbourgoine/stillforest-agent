import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from agents.content_agent import generate_post
from agents.reply_agent import generate_reply
from services.image_service import generate_multiple_images
from services.instagram_service import post_carousel_to_instagram
from services.comment_service import get_recent_posts, get_comments_on_post, reply_to_comment
from utils.logger import get_past_topics, save_post
from utils.reply_logger import has_been_replied_to, save_reply

def run_daily_post():
    print(f"\n{'='*50}")
    print(f"Running post pipeline at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    try:
        # 1. Generate content
        print("\n[1/4] Generating content...")
        past_topics = get_past_topics()
        post_data = generate_post(past_topics)
        print(f"Topic: {post_data['topic']}")
        print(f"Pillar: {post_data['content_pillar']}")
        print(f"Images to generate: {len(post_data['image_prompts'])}")
        print(f"Caption preview: {post_data['caption'][:80]}...")

        # 2. Generate and upload all images
        print("\n[2/4] Generating and uploading images...")
        image_urls = generate_multiple_images(post_data["image_prompts"])
        print(f"All {len(image_urls)} images ready.")

        # 3. Post carousel to Instagram
        print("\n[3/4] Posting carousel to Instagram...")
        instagram_id = post_carousel_to_instagram(image_urls, post_data["caption"])
        print(f"Posted! Instagram ID: {instagram_id}")

        # 4. Log it
        print("\n[4/4] Logging post...")
        save_post(
            topic=post_data["topic"],
            content_pillar=post_data["content_pillar"],
            caption=post_data["caption"],
            image_url=", ".join(image_urls),
            instagram_post_id=instagram_id
        )

        print(f"\nSuccess! Carousel post complete.")

    except Exception as e:
        print(f"\nERROR in post pipeline: {e}")

def run_comment_replies():
    print(f"\n{'='*50}")
    print(f"Checking comments at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    try:
        # Get 5 most recent posts
        posts = get_recent_posts(limit=5)
        print(f"Checking {len(posts)} recent posts for new comments...")

        total_replies = 0

        for post in posts:
            post_id = post["id"]
            post_topic = post.get("caption", "nature landscape")[:100]
            
            comments = get_comments_on_post(post_id)

            for comment in comments:
                comment_id = comment["id"]
                comment_text = comment.get("text", "")
                username = comment.get("username", "unknown")

                # Skip if already replied
                if has_been_replied_to(comment_id):
                    continue

                # Skip very short comments like just emojis
                if len(comment_text.strip()) < 3:
                    save_reply(comment_id, comment_text, 
                             "skipped", post_id, username)
                    continue

                print(f"Replying to @{username}: '{comment_text[:50]}...'")

                # Generate reply
                reply_text = generate_reply(comment_text, post_topic)
                print(f"Reply: {reply_text}")

                # Post reply
                reply_to_comment(comment_id, reply_text)

                # Log it
                save_reply(comment_id, comment_text, 
                          reply_text, post_id, username)

                total_replies += 1
                
                # Small delay between replies to be safe
                time.sleep(2)

        print(f"\nDone. Posted {total_replies} new replies.")

    except Exception as e:
        print(f"\nERROR in comment pipeline: {e}")

# Schedule daily post at 9am
schedule.every().day.at("09:00").do(run_daily_post)

# Schedule comment checks every 30 minutes
schedule.every(30).minutes.do(run_comment_replies)

if __name__ == "__main__":
    print("Stillforest Agent started.")
    print("Post scheduled daily at 9:00 AM.")
    print("Comments checked every 30 minutes.")
    print("Press Ctrl+C to stop.\n")

    # Uncomment to test posting immediately
    # run_daily_post()

    # Uncomment to test comment replies immediately
    # run_comment_replies()

    while True:
        schedule.run_pending()
        time.sleep(60)