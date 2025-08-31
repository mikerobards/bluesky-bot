import os
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

try:
    data = client.get_timeline(limit=10)
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
            embed_type = getattr(record.embed, 'py_type', str(type(record.embed)))
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
