# RSS Feed Fetcher

This Python script fetches RSS feeds from multiple URLs and prints the title and link of each entry in the feed to the console.

## Requirements

- Python 3.x

## Installation

Clone the repository or download the script file.
To run the script, ensure you have the following modules installed:

1. **feedparser**: Used to parse RSS feeds.
2. **requests**: Used to make HTTP requests for fetching feeds and sending emails.
3. **pyyaml**: Used to parse YAML configuration files.
4. **os**: Standard library module for interacting with the operating system.
5. **logging**: Standard library module for logging messages.
6. **time**: Standard library module for working with time.
7. **json**: Standard library module for working with JSON data.
8. **base64**: Standard library module for encoding and decoding binary data in base64 format.

You can install missing modules using pip, the Python package manager. For example:

```bash
pip install feedparser requests pyyaml
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
source /feedparser/venv/bin/activate
pip install feedparser requests pyyaml
deactivate
```
Create the service, with editor of your choice vim/nano/emacs
```yaml
sudo vim /etc/systemd/system/feedparser.service
```

Change the service folder /feedparser/ to the folder where the script is
```yaml
[Unit]
Description=RSS feed parser service
After=network.target

[Service]
WorkingDirectory=/feedparser/
Environment="PATH=/feedparser/venv/bin"
ExecStart=/feedparser/venv/bin/python /feedparser/feedparser.py

[Install]
WantedBy=multi-user.target
```

Reload daemon to see newly created service
```yaml
sudo systemctl daemon-reload
```
Enable the service to start on boot (after network is detected as specified in service)
```yaml
sudo systemctl enable feedparser.service
```
Start the service
```yaml
sudo systemctl start feedparser.service
```
Check status of service
```yaml
sudo systemctl status feedparser.service
```



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
