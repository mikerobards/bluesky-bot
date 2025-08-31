import os
from dotenv import load_dotenv
from atproto import Client

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

post = client.send_post('And another test post from Python.')
