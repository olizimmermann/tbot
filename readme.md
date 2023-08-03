
# TBot - Stop Phish Campaigns with Telegram Bot Flooding

TBot is a tool designed to stop phishing campaigns that use a Telegram bot as an exfiltration destination. It achieves this by generating random messages that flood the phishers' mailbox. As soon as the phishers kick out the used bot (and its token), the current phish campaign becomes useless and disarmed.

## Features

- Floods the phishers' mailbox with random messages
- Customizable message content using variables to add randomness
- Adjustable sleep time between messages to simulate real user behavior
- Option to use proxy for enhanced anonymity
- Utilizes Telegram API for bot communication

## How It Works

TBot sends a specified number of random messages to the targeted chat ID using the provided Telegram bot ID and token. The custom message can be defined in the code with variables such as P_IP, P_EMAIL, P_PASSWORD, P_ZIP, P_CITY, P_RANDHIGHINT, and P_ORG, which are substituted with random values during execution.

## Requirements

- Python 3.x
- `requests` library
- `pathlib` library

## Installation

1. Clone the TBot repository:

```
git clone https://github.com/olizimmermann/tbot.git
cd TBot
```

2. Install the required dependencies:

```
pip install requests
pip install pathlib
```

## Command Line Options

```bash
python3 tbot.py --bot-id <bot-id> --token <token> --chat-id <chat-id>
```

- `-h`, `--help`: Show the help message and exit.
- `--bot-id BOT_ID`: ID of the Telegram bot to use for communication.
- `--token TOKEN`: Token of the Telegram bot.
- `--chat-id CHAT_ID`: Chat ID of the target.
- `--messages MESSAGES`: Amount of messages to send (optional, default is 10).
- `--text TEXT`: Define a custom message to send (optional). Use variables inside to make it random (e.g., P_IP, P_EMAIL, P_PASSWORD, P_ZIP, P_CITY, P_RANDHIGHINT, P_ORG).
- `--min-sleep MIN_SLEEP`: Minimum sleep time between messages (optional, default is 1 second).
- `--max-sleep MAX_SLEEP`: Maximum sleep time between messages (optional, default is 5 seconds).
- `--disable-check`: Disable connectivity check to the Telegram API (optional).
- `--name-list NAME_LIST`: First Names Wordlist (optional).
- `--surname-list SURNAME_LIST`: Last Names Wordlist (optional).
- `--domain-list DOMAIN_LIST`: Domains Wordlist (optional).
- `--city-list CITY_LIST`: City Wordlist (optional).
- `--proxy PROXY`: Proxy address (without port) to use for requests (optional).
- `--proxy-port PORT`: Proxy port to use (optional).

## Usage Example

To run TBot with the required parameters:

```bash
python3 tbot.py --bot-id <phishers-telegram-bot-id> --token <phishers-telegram-bot-token> --chat-id <target-chat-id>
```

## Disclaimer

Using this tool to flood any mailbox, including phishers', may have legal consequences. Please use this tool responsibly and only in accordance with the applicable laws and regulations.
