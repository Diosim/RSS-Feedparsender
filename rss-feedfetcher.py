# Steps to do for this to work
# 1. Create free mailjet account (limit of 200 emails per day) https://www.mailjet.com/
# 2. Buy a domain https://www.cloudflare.com/ ~10usd per year
# 3. Add TXT DNS records to Cloudflare account for SPF and DKIM


import feedparser
import requests
import time
import json
from base64 import b64encode
import logging
import sys
import yaml
import os  # Import the os module
#import pdb # For debugging mode

with open(".env", "r") as f:
    env_data = yaml.safe_load(f)
    
# Set up logging DEBUG | INFO | WARNING | ERROR | CRITICAL
logging.basicConfig(filename='script.log', level=logging.INFO)
# Log the current working directory
logging.info(f"Current working directory: {os.getcwd()}")

# Check if seen_posts.log already exists
if not os.path.exists('seen_posts.log'):
    try:
        # If it doesn't exist, create it
        with open('seen_posts.log', 'a') as file:
            logging.info("Created seen_posts.log file successfully")  # Log success
    except Exception as e:
        logging.error(f"Error creating seen_posts.log file: {e}")  # Log error
else:
    logging.info("seen_posts.log file already exists")  # Log existing file

# Extract RSS URLs from environment variables
rss_urls = env_data["RSS_URLS"]


def fetch_feed(url):
    try:
        logging.info(f"Fetching RSS feed from {url}")
        return feedparser.parse(url)
    except Exception as e:
        logging.error(f"Error fetching RSS feed from {url}: {e}")
        return None

def is_new_post(post_id, seen_posts):
    return post_id not in seen_posts

def load_seen_posts():
    try:
        with open('seen_posts.log', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        logging.error("seen_posts.log file not found.")
        return []

    
def update_seen_posts(post_id):
    try:
        # Load existing seen posts
        seen_posts = load_seen_posts()
        # Check if the post ID is already in the seen posts
        if post_id not in seen_posts:
            with open('seen_posts.log', 'a') as file:
                logging.info(f"Writting RSS feed from {post_id}")
                file.write(post_id + '\n')
    except Exception as e:
        logging.error(f"Error updating seen_posts.log: {e}")



def send_email(new_posts):
    api_key = env_data["API_KEY"]
    api_secret = env_data["SECRET_KEY"]
    sender_email = env_data["SENDER_EMAIL"]
    receiver_emails = env_data["RECEIVER_EMAILS"]
    sender_email_name = env_data["SENDER_EMAIL_NAME"]
    email_subject = env_data["EMAIL_SUBJECT"]

    api_url = "https://api.mailjet.com/v3.1/send"

    encoded_credentials = b64encode(f"{api_key}:{api_secret}".encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    body = "New RSS feed notification: \n"
    for post in new_posts:
        body += f"{post['title']} - {post['link']}\n"
        if 'description' in post:
            body += f"Description: {post['description']}\n"
        else:
            body += "Description: N/A\n"
        body += "\n"

    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": sender_email_name
                },
                "To": [{"Email": email} for email in receiver_emails],
                "Subject": email_subject,
                "TextPart": body,
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def check_feeds_and_notify():
    seen_posts = load_seen_posts()
    new_posts = []

    try:
        for url in rss_urls:
            feed = fetch_feed(url)
            if feed is None:
                logging.warning(f"Failed to fetch feed from {url}. Skipping to the next feed.")
                continue  # Skip to the next feed if fetching failed

            for entry in feed.entries:
                if is_new_post(entry.id, seen_posts):
                    logging.info(f"Updating with new feeds: {entry.id}")
                    new_posts.append({'title': entry.title, 'link': entry.link})
                    update_seen_posts(entry.id)
                    # Enable debugging
                    #pdb.set_trace()
    except Exception as e:
        logging.error(f"Error checking feeds and notifying: {e}")
    else:
        if new_posts:
            logging.info(f"Found {len(new_posts)} new posts. Sending email notifications.")
            send_email(new_posts)
        else:
            logging.info("No new posts found.")

    logging.info("Completed checking feeds and notifying.")


if __name__ == "__main__":
    while True:
        try:
            check_feeds_and_notify()
            print("Waiting for the next check...", file=sys.stderr)
            #print("Waiting for the next check...")
            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            break  # Exit the loop if an unexpected error occurs
