# RSS Feed Fetcher

This Python script fetches RSS feeds from multiple URLs and prints the title and link of each entry in the feed to the console.

## Requirements

- Python 3.x
- `feedparser` library

## Installation

1. Clone the repository or download the script file.
2. Install the `feedparser` library using pip:

## Configuration

Create a .env file in the same folder with the script with the structure below:

API_KEY: XXXXX

SECRET_KEY: XXXXX

SENDER_EMAIL: user@mail.com

SENDER_EMAIL_NAME: "sender name"

EMAIL_SUBJECT: "Put your email subject here"

RECEIVER_EMAILS:
  - user1@example.com
  - user2@example.com"

RSS_URLS:
  - feedURL1
  - feedURL2
  - feedURL3

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
