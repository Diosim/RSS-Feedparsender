# RSS Feed Fetcher

This Python script fetches RSS feeds from multiple URLs and prints the title and link of each entry in the feed to the console.
The method of sending emails is using the mailjet API, for other mail services changes will have to be made to the send_email function.

## Requirements

- Python 3.x

## Installation

Clone the repository or download the script file.
To run the script, ensure you have the following modules installed:

01. **feedparser**: Used to parse RSS feeds.
02. **requests**: Used to make HTTP requests for fetching feeds and sending emails.
03. **pyyaml**: Used to parse YAML configuration files.
04. **os**: Standard library module for interacting with the operating system.
05. **logging**: Standard library module for logging messages.
06. **time**: Standard library module for working with time.
07. **json**: Standard library module for working with JSON data.
08. **base64**: Standard library module for encoding and decoding binary data in base64 format.
09. **bs4**: A Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree.
10. **html**: A standard library module in Python that provides utilities to manipulate HTML. It includes functions to escape and unescape HTML entities and convert characters to their HTML-safe sequences.

You can install missing modules using pip, the Python package manager. For example:

```bash
pip install feedparser requests pyyaml bs4
```

## Configuration

Create a .env file in the same folder with the script with the structure below:
```yaml
API_KEY: XXXXX
SECRET_KEY: XXXXX
SENDER_EMAIL: user@yourmail.com
SENDER_EMAIL_NAME: "your sender name"
EMAIL_SUBJECT: "Put your email subject here"
RECEIVER_EMAILS:
  - user1@example.com
  - user2@example.com
RSS_URLS:
  - feedURL1
  - feedURL2
  - feedURL3
```
## Setting up the script as a service on Linux
Setup a venv in the folder where script is located
```yaml
source /rss-feedfetcher/venv/bin/activate
pip install feedparser requests pyyaml bs4
deactivate
```
Create the service, with editor of your choice vim/nano/emacs
```yaml
sudo vim /etc/systemd/system/rss-feedfetcher.service
```

Change the service folder /rss-feedfetcher/ to the folder where the script is
```yaml
[Unit]
Description=RSS feed fetcher service
After=network.target

[Service]
WorkingDirectory=/rss-feedfetcher/
Environment="PATH=/rss-feedfetcher/venv/bin"
ExecStart=/rss-feedfetcher/venv/bin/python /rss-feedfetcher/rss-feedfetcher.py

[Install]
WantedBy=multi-user.target
```

Reload daemon to see newly created service
```yaml
sudo systemctl daemon-reload
```
Enable the service to start on boot (after network is detected as specified in service)
```yaml
sudo systemctl enable rss-feedfetcher.service
```
Start the service
```yaml
sudo systemctl start rss-feedfetcher.service
```
Check status of service
```yaml
sudo systemctl status rss-feedfetcher.service
```

## Future additions
- Add formatting to sent emails
- Change receivers list to be BCC
- Add dates to each post when sending emails

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
