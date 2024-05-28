import feedparser
import requests
import time
import json
from base64 import b64encode
import logging
import sys
import yaml
import os
from bs4 import BeautifulSoup
import html
from datetime import datetime

# Set up logging INFO | ERROR | WARNING
logging.basicConfig(filename='script.log', level=logging.ERROR)
logging.info(f"Current working directory: {os.getcwd()}")

if os.path.isfile(".env"):
    with open(".env", "r", encoding='utf-8') as f:
        env_data = yaml.safe_load(f)
else:
    logging.error(".env not found")
    print(".env not found")
    
# Function to clean HTML from RSS feeds
def clean_html(html_string):
    unescaped = html.unescape(html_string)
    soup = BeautifulSoup(unescaped, "html.parser")
    return soup.get_text()

if not os.path.exists('seen_posts.log'):
    try:
        with open('seen_posts.log', 'a') as file:
            logging.info("Created seen_posts.log file successfully")
    except Exception as e:
        logging.error(f"Error creating seen_posts.log file: {e}")

def load_html_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def fill_html_template(template, date, posts):
    return template.replace('{{date}}', date).replace('{{posts}}', posts)

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
        seen_posts = load_seen_posts()
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
    template_path = 'email_template.html'

    api_url = "https://api.mailjet.com/v3.1/send"
    encoded_credentials = b64encode(f"{api_key}:{api_secret}".encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    template = load_html_template(template_path)
    date = datetime.now().strftime('%d-%m-%Y')
    posts_content = ""

    for post in new_posts:
        posts_content += f"<p><a href='{post['link']}'>{post['title']}</a><br>{clean_html(post['description'])}</p>"

    body = fill_html_template(template, date, posts_content)

    for email in receiver_emails:
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": sender_email,
                        "Name": sender_email_name
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": email.split('@')[0]
                        }
                    ],
                    "Subject": email_subject,
                    "HTMLPart": body,
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
        for url in env_data["RSS_URLS"]:
            feed = fetch_feed(url)
            if feed is None:
                logging.warning(f"Failed to fetch feed from {url}. Skipping to the next feed.")
                continue

            for entry in feed.entries:
                if is_new_post(entry.id, seen_posts):
                    logging.info(f"Updating with new feeds: {entry.id}")
                    new_posts.append({'title': entry.title, 'link': entry.link, 'description': entry.description})
                    update_seen_posts(entry.id)
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
            time.sleep(300)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            break
