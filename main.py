import os
import time
from dotenv import load_dotenv
from atproto import Client
from atproto.exceptions import NetworkError

# Load environment variables from .env file
load_dotenv()

# Load credentials from environment variables
username = os.getenv('BLUESKY_USERNAME')
password = os.getenv('BLUESKY_PASSWORD')

if not username or not password:
    raise ValueError(
        "Please set BLUESKY_USERNAME and BLUESKY_PASSWORD environment variables")

client = Client()
login = client.login(username, password)
print(login.handle, login.display_name, login.followers_count)

# post = client.send_post('And another test post from Python.')


# Feed
try:
    data = client.get_timeline(limit=1)
    feed = data.feed
    next_page = data.cursor

    for item in feed:
        post = item.post
        author = post.author
        record = post.record

        # Display author info
        print(f"@{author.handle} ({author.display_name})")

        # Display post content
        print(f"{record.text}")

        # Display engagement metrics
        likes = getattr(post, 'like_count', 0)
        reposts = getattr(post, 'repost_count', 0)
        replies = getattr(post, 'reply_count', 0)
        print(f"💙 {likes} | 🔄 {reposts} | 💬 {replies}")

        # Display timestamp
        print(f"Posted: {record.created_at}")

        # Check for embedded content
        if hasattr(record, 'embed') and record.embed:
            embed_type = getattr(record.embed, 'py_type',
                                 str(type(record.embed)))
            if 'images' in embed_type:
                images = getattr(record.embed, 'images', [])
                print(f"📷 Contains {len(images)} image(s)")
            elif 'external' in embed_type:
                external = getattr(record.embed, 'external', None)
                if external:
                    title = getattr(external, 'title', 'Link')
                    print(f"🔗 Link: {title}")

        print("-" * 50)

except NetworkError as error:
    print(f"something went wrong:{error} ")

# Generous Bot


def limit_handler(follower_bundle):
    try:
        while True and len(follower_bundle.followers) > 0:
            yield follower_bundle.followers.pop()
    except NetworkError as error:
        time.sleep(1000)


followers = client.get_followers(login.did)
for follower in limit_handler(followers):
    print(f"follower: {follower.display_name}")
    if follower.display_name == "follower":
        client.follow(follower.did)

# Like Bot

search_string = 'hello'
numberOfPosts = 5
count = 0
try:
    like_bot_data = client.get_timeline(limit=100)
    like_bot_feed = like_bot_data.feed

    for item in like_bot_feed:
        if item.post.record.text.find(search_string) > -1:
            count += 1
            client.like(item.post.uri, item.post.cid)
            print(item.post.uri, item.post.cid)
            print('I liked that tweet!')
            if count >= numberOfPosts:
                break
except NetworkError as e:
    print(f"Network error in Like Bot: {e}")
except Exception as e:
    print(f"Error in Like Bot: {e}")
