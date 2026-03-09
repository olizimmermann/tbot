import os
import sys
import time
import json
import requests
import random
import string
import pathlib
import argparse
import urllib.parse
from datetime import datetime


header = r"""
_________ ______   _______ _________
\__   __/(  ___ \ (  ___  )\__   __/
   ) (   | (   ) )| (   ) |   ) (   
   | |   | (__/ / | |   | |   | |   
   | |   |  __ (  | |   | |   | |   
   | |   | (  \ \ | |   | |   | |   
   | |   | )___) )| (___) |   | |   
   )_(   |/ \___/ (_______)   )_( by OZ  
                                    
"""
print(header)

# ─────────────────────────────────────────────
# Built-in fallback wordlists
# ─────────────────────────────────────────────
DEFAULT_NAMES = ["James", "John", "Robert", "Michael", "David", "Sarah", "Jessica", "Emily", "Ashley", "Amanda",
                 "Chris", "Daniel", "Matthew", "Andrew", "Laura", "Jennifer", "Linda", "Patricia", "Elizabeth", "Susan"]
DEFAULT_SURNAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Taylor",
                    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Moore", "Young", "Allen"]
DEFAULT_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com", "icloud.com",
                   "aol.com", "mail.com", "zoho.com", "yandex.com"]
DEFAULT_CITIES = ["Berlin", "London", "Paris", "NewYork", "Tokyo", "Sydney", "Toronto", "Madrid", "Rome", "Vienna",
                  "Amsterdam", "Brussels", "Prague", "Warsaw", "Oslo", "Helsinki", "Dublin", "Lisbon", "Athens", "Zurich"]


# ─────────────────────────────────────────────
# Core API helper
# ─────────────────────────────────────────────
class TelegramAPI:
    """Wrapper for Telegram Bot API calls."""

    def __init__(self, bot_id, token, proxy=None):
        self.base_url = f"https://api.telegram.org/bot{bot_id}:{token}"
        self.bot_id = bot_id
        self.token = token
        self.proxy = proxy or {'http': None, 'https': None}

    def call(self, method, params=None, quiet=False):
        """Make a GET request to the Telegram Bot API."""
        url = f"{self.base_url}/{method}"
        try:
            r = requests.get(url, params=params, proxies=self.proxy, timeout=30)
            data = r.json()
            if not data.get('ok'):
                if not quiet:
                    print(f"[ERROR] {method}: {data.get('description', 'Unknown error')} (code: {data.get('error_code')})")
                return None
            return data.get('result')
        except requests.exceptions.RequestException as e:
            if not quiet:
                print(f"[ERROR] Connection failed for {method}: {e}")
            return None
        except json.JSONDecodeError:
            if not quiet:
                print(f"[ERROR] Invalid JSON response from {method}")
            return None

    def post(self, method, data=None, quiet=False):
        """Make a POST request to the Telegram Bot API."""
        url = f"{self.base_url}/{method}"
        try:
            r = requests.post(url, json=data, proxies=self.proxy, timeout=30)
            resp = r.json()
            if not resp.get('ok'):
                if not quiet:
                    print(f"[ERROR] {method}: {resp.get('description', 'Unknown error')} (code: {resp.get('error_code')})")
                return None
            return resp.get('result')
        except requests.exceptions.RequestException as e:
            if not quiet:
                print(f"[ERROR] Connection failed for {method}: {e}")
            return None
        except json.JSONDecodeError:
            if not quiet:
                print(f"[ERROR] Invalid JSON response from {method}")
            return None

    def download_url(self, file_path):
        """Build a file download URL."""
        return f"https://api.telegram.org/file/bot{self.bot_id}:{self.token}/{file_path}"


# ─────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────
def pp(obj, indent=2):
    """Pretty print JSON."""
    print(json.dumps(obj, indent=indent, ensure_ascii=False))

def get_list(path, name='wordlist'):
    wordlist = []
    if not os.path.isfile(path):
        sys.exit(f"File {name} at {path} not found!")
    with open(path, "r") as f:
        for line in f.readlines():
            wordlist.append(line.replace('\n', ''))
    return wordlist

def random_pw(s=8, e=12):
    n = random.randint(s, e)
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=n))

def random_email(name, family_name, domain_list):
    return f'{random.choice(name).lower()}.{random.choice(family_name).lower()}@{random.choice(domain_list)}'

def build_proxy(proxy_addr, proxy_port):
    if proxy_addr and proxy_port:
        return {'http': f'http://{proxy_addr}:{proxy_port}', 'https': f'https://{proxy_addr}:{proxy_port}'}
    return {'http': None, 'https': None}

def format_timestamp(ts):
    """Convert unix timestamp to readable date."""
    if ts:
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return 'N/A'


# ─────────────────────────────────────────────
# Command handlers
# ─────────────────────────────────────────────

def cmd_recon(api, args):
    """Full recon: getMe + getWebhookInfo."""
    print("=" * 60)
    print("  BOT RECON")
    print("=" * 60)

    # getMe
    print("\n[*] Fetching bot info (getMe)...")
    me = api.call('getMe')
    if me:
        print(f"  Bot ID:        {me.get('id')}")
        print(f"  Name:          {me.get('first_name', '')} {me.get('last_name', '')}")
        print(f"  Username:      @{me.get('username', 'N/A')}")
        print(f"  Can join groups:       {me.get('can_join_groups', 'N/A')}")
        print(f"  Can read all msgs:     {me.get('can_read_all_group_messages', 'N/A')}")
        print(f"  Supports inline:       {me.get('supports_inline_queries', 'N/A')}")
        print(f"  Can connect business:  {me.get('can_connect_to_business', 'N/A')}")
    else:
        print("  Failed to fetch bot info. Token may be invalid.")
        return

    # getWebhookInfo
    print("\n[*] Fetching webhook info (getWebhookInfo)...")
    wh = api.call('getWebhookInfo')
    if wh:
        webhook_url = wh.get('url', '')
        print(f"  Webhook URL:           {webhook_url if webhook_url else '(none - using getUpdates)'}")
        print(f"  Pending updates:       {wh.get('pending_update_count', 0)}")
        print(f"  Custom certificate:    {wh.get('has_custom_certificate', False)}")
        print(f"  Max connections:       {wh.get('max_connections', 'N/A')}")
        print(f"  Allowed updates:       {wh.get('allowed_updates', 'all (default)')}")
        if wh.get('last_error_date'):
            print(f"  Last error:            {format_timestamp(wh['last_error_date'])}")
            print(f"  Last error message:    {wh.get('last_error_message', 'N/A')}")
        if wh.get('ip_address'):
            print(f"  Webhook IP:            {wh['ip_address']}")

        if webhook_url:
            print(f"\n  [!] WEBHOOK IS ACTIVE: {webhook_url}")
            print("  [!] This means getUpdates won't work. Use 'delete-webhook' first.")
    print()


def cmd_read(api, args):
    """Read incoming messages via getUpdates."""
    print("[*] Fetching updates (getUpdates)...")
    params = {
        'limit': args.limit,
        'timeout': args.timeout,
    }
    if args.offset:
        params['offset'] = args.offset

    result = api.call('getUpdates', params)
    if result is None:
        print("[!] Failed. If a webhook is set, run 'delete-webhook' first.")
        return

    if not result:
        print("[*] No new updates found.")
        return

    print(f"[*] Found {len(result)} update(s):\n")
    for update in result:
        uid = update.get('update_id')
        msg = update.get('message') or update.get('channel_post') or update.get('edited_message') or {}

        if msg:
            sender = msg.get('from', {})
            chat = msg.get('chat', {})
            text = msg.get('text', '<non-text message>')
            date = format_timestamp(msg.get('date'))

            sender_name = f"{sender.get('first_name', '')} {sender.get('last_name', '')}".strip()
            sender_user = sender.get('username', '')
            chat_title = chat.get('title', chat.get('first_name', 'DM'))
            chat_id = chat.get('id', 'N/A')

            print(f"  [{uid}] {date}")
            print(f"    From: {sender_name} (@{sender_user}) | ID: {sender.get('id', 'N/A')}")
            print(f"    Chat: {chat_title} | Chat ID: {chat_id} | Type: {chat.get('type', 'N/A')}")
            print(f"    Text: {text}")

            # Show if there are photos, documents, etc.
            if msg.get('photo'):
                print(f"    [+] Contains photo ({len(msg['photo'])} sizes)")
            if msg.get('document'):
                print(f"    [+] Contains document: {msg['document'].get('file_name', 'unnamed')}")
            if msg.get('sticker'):
                print(f"    [+] Contains sticker: {msg['sticker'].get('emoji', '')}")
            if msg.get('location'):
                loc = msg['location']
                print(f"    [+] Contains location: {loc.get('latitude')}, {loc.get('longitude')}")
            print()
        else:
            # Could be callback_query, inline_query, etc.
            print(f"  [{uid}] Non-message update:")
            for key in update:
                if key != 'update_id':
                    print(f"    Type: {key}")
            print()


def cmd_chat_info(api, args):
    """Get full chat info via getChat."""
    print(f"[*] Fetching chat info for: {args.chat_id}")
    result = api.call('getChat', {'chat_id': args.chat_id})
    if result:
        print(f"  Chat ID:         {result.get('id')}")
        print(f"  Type:            {result.get('type')}")
        print(f"  Title:           {result.get('title', 'N/A')}")
        print(f"  Username:        @{result.get('username', 'N/A')}")
        print(f"  First name:      {result.get('first_name', 'N/A')}")
        print(f"  Last name:       {result.get('last_name', 'N/A')}")
        print(f"  Description:     {result.get('description', 'N/A')}")
        print(f"  Invite link:     {result.get('invite_link', 'N/A')}")

        if result.get('photo'):
            print(f"  Has photo:       Yes")
        if result.get('pinned_message'):
            pinned = result['pinned_message']
            print(f"  Pinned message:  {pinned.get('text', '<non-text>')[:100]}")

        print(f"\n  [Full JSON]:")
        pp(result)


def cmd_admins(api, args):
    """List chat administrators via getChatAdministrators."""
    print(f"[*] Fetching admins for chat: {args.chat_id}")
    result = api.call('getChatAdministrators', {'chat_id': args.chat_id})
    if result:
        print(f"[*] Found {len(result)} administrator(s):\n")
        for admin in result:
            user = admin.get('user', {})
            name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
            print(f"  {admin.get('status', 'admin'):12s} | {name:20s} | @{user.get('username', 'N/A'):15s} | ID: {user.get('id')}")
            if user.get('is_bot'):
                print(f"               [BOT]")
    else:
        print("[!] Failed. Bot may not be in the chat or may not have permission.")


def cmd_member_count(api, args):
    """Get member count via getChatMemberCount."""
    print(f"[*] Fetching member count for chat: {args.chat_id}")
    result = api.call('getChatMemberCount', {'chat_id': args.chat_id})
    if result is not None:
        print(f"  Members: {result}")


def cmd_get_member(api, args):
    """Get info about a specific member via getChatMember."""
    print(f"[*] Fetching member {args.user_id} in chat {args.chat_id}")
    result = api.call('getChatMember', {'chat_id': args.chat_id, 'user_id': args.user_id})
    if result:
        user = result.get('user', {})
        name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        print(f"  Name:      {name}")
        print(f"  Username:  @{user.get('username', 'N/A')}")
        print(f"  User ID:   {user.get('id')}")
        print(f"  Is bot:    {user.get('is_bot', False)}")
        print(f"  Status:    {result.get('status')}")
        print(f"  Premium:   {user.get('is_premium', False)}")
        print(f"\n  [Full JSON]:")
        pp(result)


def cmd_delete_webhook(api, args):
    """Remove webhook via deleteWebhook."""
    print("[*] Deleting webhook...")
    params = {}
    if args.drop_pending:
        params['drop_pending_updates'] = True
    result = api.call('deleteWebhook', params)
    if result:
        print("[+] Webhook deleted successfully!")
        print("    You can now use 'read' (getUpdates) to fetch messages.")
    else:
        print("[!] Failed to delete webhook.")


def cmd_get_webhook(api, args):
    """Get webhook info via getWebhookInfo."""
    print("[*] Fetching webhook info...")
    result = api.call('getWebhookInfo')
    if result:
        pp(result)


def cmd_send(api, args):
    """Send a message via sendMessage."""
    params = {
        'chat_id': args.chat_id,
        'text': args.text,
    }
    if args.parse_mode:
        params['parse_mode'] = args.parse_mode
    if args.silent:
        params['disable_notification'] = True

    result = api.call('sendMessage', params)
    if result:
        print(f"[+] Message sent! Message ID: {result.get('message_id')}")
    else:
        print("[!] Failed to send message.")


def cmd_delete_msg(api, args):
    """Delete a message via deleteMessage."""
    print(f"[*] Deleting message {args.message_id} in chat {args.chat_id}...")
    result = api.call('deleteMessage', {'chat_id': args.chat_id, 'message_id': args.message_id})
    if result:
        print("[+] Message deleted.")
    else:
        print("[!] Failed to delete message. Bot may not have permission.")


def cmd_forward(api, args):
    """Forward a message via forwardMessage."""
    params = {
        'chat_id': args.to_chat_id,
        'from_chat_id': args.from_chat_id,
        'message_id': args.message_id,
    }
    result = api.call('forwardMessage', params)
    if result:
        print(f"[+] Message forwarded! New message ID: {result.get('message_id')}")
    else:
        print("[!] Failed to forward message.")


def cmd_set_webhook(api, args):
    """Set a webhook via setWebhook."""
    print(f"[*] Setting webhook to: {args.url}")
    params = {'url': args.url}
    if args.secret_token:
        params['secret_token'] = args.secret_token
    result = api.call('setWebhook', params)
    if result:
        print(f"[+] Webhook set to: {args.url}")
    else:
        print("[!] Failed to set webhook.")


def cmd_logout(api, args):
    """Log out bot from cloud Bot API via logOut."""
    print("[*] Logging out bot from Telegram Bot API server...")
    result = api.call('logOut')
    if result:
        print("[+] Bot logged out. It cannot be used for 10 minutes.")
    else:
        print("[!] Failed to log out.")


def cmd_get_file(api, args):
    """Get file download link via getFile."""
    print(f"[*] Fetching file info for: {args.file_id}")
    result = api.call('getFile', {'file_id': args.file_id})
    if result:
        file_path = result.get('file_path', '')
        download_url = api.download_url(file_path)
        print(f"  File ID:       {result.get('file_id')}")
        print(f"  File unique:   {result.get('file_unique_id')}")
        print(f"  File size:     {result.get('file_size', 'N/A')} bytes")
        print(f"  File path:     {file_path}")
        print(f"  Download URL:  {download_url}")


def cmd_ban(api, args):
    """Ban a user from chat via banChatMember."""
    print(f"[*] Banning user {args.user_id} from chat {args.chat_id}...")
    params = {'chat_id': args.chat_id, 'user_id': args.user_id}
    result = api.call('banChatMember', params)
    if result:
        print(f"[+] User {args.user_id} banned.")
    else:
        print("[!] Failed. Bot may not have admin rights.")


def cmd_unban(api, args):
    """Unban a user from chat via unbanChatMember."""
    print(f"[*] Unbanning user {args.user_id} from chat {args.chat_id}...")
    params = {'chat_id': args.chat_id, 'user_id': args.user_id, 'only_if_banned': True}
    result = api.call('unbanChatMember', params)
    if result:
        print(f"[+] User {args.user_id} unbanned.")
    else:
        print("[!] Failed. Bot may not have admin rights.")


def cmd_pin(api, args):
    """Pin a message via pinChatMessage."""
    print(f"[*] Pinning message {args.message_id} in chat {args.chat_id}...")
    params = {'chat_id': args.chat_id, 'message_id': args.message_id}
    if args.silent:
        params['disable_notification'] = True
    result = api.call('pinChatMessage', params)
    if result:
        print("[+] Message pinned.")
    else:
        print("[!] Failed. Bot may not have admin rights.")


def cmd_unpin(api, args):
    """Unpin a message via unpinChatMessage."""
    print(f"[*] Unpinning message in chat {args.chat_id}...")
    params = {'chat_id': args.chat_id}
    if args.message_id:
        params['message_id'] = args.message_id
    result = api.call('unpinChatMessage', params)
    if result:
        print("[+] Message unpinned.")
    else:
        print("[!] Failed.")


def cmd_leave(api, args):
    """Leave a chat via leaveChat."""
    print(f"[*] Leaving chat {args.chat_id}...")
    result = api.call('leaveChat', {'chat_id': args.chat_id})
    if result:
        print("[+] Bot left the chat.")
    else:
        print("[!] Failed to leave chat.")


def cmd_set_title(api, args):
    """Set chat title via setChatTitle."""
    print(f"[*] Setting chat title for {args.chat_id}...")
    result = api.call('setChatTitle', {'chat_id': args.chat_id, 'title': args.title})
    if result:
        print(f"[+] Chat title set to: {args.title}")
    else:
        print("[!] Failed. Bot may not have admin rights.")


def cmd_set_description(api, args):
    """Set chat description via setChatDescription."""
    print(f"[*] Setting chat description for {args.chat_id}...")
    result = api.call('setChatDescription', {'chat_id': args.chat_id, 'description': args.description})
    if result:
        print("[+] Chat description updated.")
    else:
        print("[!] Failed.")


def cmd_export_invite(api, args):
    """Export invite link via exportChatInviteLink."""
    print(f"[*] Exporting invite link for chat {args.chat_id}...")
    result = api.call('exportChatInviteLink', {'chat_id': args.chat_id})
    if result:
        print(f"  Invite link: {result}")
    else:
        print("[!] Failed. Bot may not have admin rights.")


def cmd_raw(api, args):
    """Call any arbitrary Bot API method with optional JSON params."""
    print(f"[*] Calling raw API method: {args.method}")
    params = None
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError:
            print("[!] Invalid JSON params.")
            return
    result = api.call(args.method, params)
    if result is not None:
        pp(result)
    else:
        print("[!] Method call failed or returned no result.")


def cmd_monitor(api, args):
    """Continuously monitor for new messages (polling loop)."""
    print(f"[*] Monitoring for updates (poll every {args.interval}s, Ctrl+C to stop)...")

    # First check for webhook
    wh = api.call('getWebhookInfo', quiet=True)
    if wh and wh.get('url'):
        print(f"[!] Webhook is active: {wh['url']}")
        print("[!] Cannot use getUpdates while webhook is set. Run 'delete-webhook' first.")
        return

    offset = None
    count = 0
    try:
        while True:
            params = {'limit': 100, 'timeout': 5}
            if offset:
                params['offset'] = offset

            result = api.call('getUpdates', params, quiet=True)
            if result:
                for update in result:
                    count += 1
                    uid = update.get('update_id')
                    offset = uid + 1  # Mark as read

                    msg = update.get('message') or update.get('channel_post') or update.get('edited_message') or {}
                    if msg:
                        sender = msg.get('from', {})
                        text = msg.get('text', '<non-text>')
                        date = format_timestamp(msg.get('date'))
                        sender_name = f"{sender.get('first_name', '')} {sender.get('last_name', '')}".strip()
                        chat = msg.get('chat', {})
                        chat_title = chat.get('title', chat.get('first_name', 'DM'))

                        print(f"  [{date}] ({chat_title}) {sender_name}: {text}")

                        if msg.get('photo'):
                            print(f"           [photo attached]")
                        if msg.get('document'):
                            print(f"           [document: {msg['document'].get('file_name', 'unnamed')}]")
                    else:
                        for key in update:
                            if key != 'update_id':
                                print(f"  [update] Type: {key}")

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print(f"\n[*] Stopped monitoring. Received {count} update(s).")


def cmd_spam(api, args):
    """Original TBot spam functionality."""
    # Load wordlists
    if args.name_list:
        if not os.path.isfile(args.name_list):
            sys.exit(f'File not found: {args.name_list}')
        name_list = get_list(pathlib.Path(args.name_list), name='First Name List')
    else:
        name_list = DEFAULT_NAMES
        print("Using built-in default name list.")

    if args.surname_list:
        if not os.path.isfile(args.surname_list):
            sys.exit(f'File not found: {args.surname_list}')
        family_name_list = get_list(pathlib.Path(args.surname_list), name='Last Name List')
    else:
        family_name_list = DEFAULT_SURNAMES
        print("Using built-in default surname list.")

    if args.domain_list:
        if not os.path.isfile(args.domain_list):
            sys.exit(f'File not found: {args.domain_list}')
        domain_list = get_list(pathlib.Path(args.domain_list), name='Domain List')
    else:
        domain_list = DEFAULT_DOMAINS
        print("Using built-in default domain list.")

    if args.city_list:
        if not os.path.isfile(args.city_list):
            sys.exit(f'File not found: {args.city_list}')
        city_list = get_list(pathlib.Path(args.city_list), name='City List')
    else:
        city_list = DEFAULT_CITIES
        print("Using built-in default city list.")

    def create_msg(text=None):
        P_EMAIL = random_email(name_list, family_name_list, domain_list)
        P_PASSWORD = random_pw()
        P_IP = f"{random.randint(11,230)}.{random.randint(11,230)}.{random.randint(11,230)}.{random.randint(11,230)}"
        P_ZIP = random.randint(1000, 88999)
        P_COUNTRYCODE = "".join(random.choices(string.ascii_uppercase, k=2))
        P_CITY = random.choice(city_list)
        P_RANDHIGHINT = str(random.randint(20000, 22000000))
        P_ORG = random.choice(family_name_list) + "-" + random.choice(family_name_list)
        today = datetime.now().strftime('%d/%m/%Y')

        default = f"""<b>OFFICE365-HTML-LOGS@ZERO</b>
    [1] {today}
    <b>USER-AGENT: </b>Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/P_RANDHIGHINT Firefox/P_RANDHIGHINT.0
    <a>pwned</a>
    <b>EMAIL: </b><pre>P_EMAIL</pre>
    <b>PASSWORD: </b><a>P_PASSWORD</a>
    <b>Location: </b>IP: P_IP | CITY: P_CITY | COUNTRY: P_COUNTRYCODE | ORG: P_ORG | POSTAL: P_ZIP&parse_mode=html HTTP/2"""

        if text is None:
            text = default

        text = text.replace('P_EMAIL', P_EMAIL).replace('P_PASSWORD', P_PASSWORD).replace('P_IP', P_IP)
        text = text.replace('P_ZIP', str(P_ZIP)).replace('P_COUNTRYCODE', P_COUNTRYCODE)
        text = text.replace('P_CITY', P_CITY).replace('P_RANDHIGHINT', P_RANDHIGHINT).replace("P_ORG", P_ORG)
        text = urllib.parse.quote_plus(text)
        return text, P_EMAIL

    def send_message_raw(msg):
        """Use raw URL (original behavior for spam compatibility)."""
        url = f"{api.base_url}/sendMessage?chat_id=-{args.chat_id}&text={msg}"
        r = requests.get(url, proxies=api.proxy)
        return r.status_code

    max_msgs = args.messages
    print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\t\tStarting phishers payback..')
    start = time.time()

    for i in range(max_msgs):
        try:
            txt, email = create_msg(args.text)
            ret = send_message_raw(txt)
            time.sleep(random.randint(args.min_sleep, args.max_sleep))
            print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\t{ret}\tSending {i+1}/{max_msgs} [{email}]')
            if ret > 400:
                end = time.time()
                duration = end - start
                unit = "s"
                if duration >= 3600:
                    duration = duration / 3600
                    unit = "h"
                elif duration >= 60:
                    duration = duration / 60
                    unit = "m"
                print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\t\tBot disabled after {i+1} messages. [{duration:.1f}{unit}]')
                sys.exit(0)
        except KeyboardInterrupt:
            end = time.time()
            duration = end - start
            unit = "s"
            if duration >= 3600:
                duration = duration / 3600
                unit = "h"
            elif duration >= 60:
                duration = duration / 60
                unit = "m"
            print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\t\tStopped after {i+1} messages. [{duration:.1f}{unit}]')
            sys.exit(0)

    end = time.time()
    duration = end - start
    unit = "s"
    if duration >= 3600:
        duration = duration / 3600
        unit = "h"
    elif duration >= 60:
        duration = duration / 60
        unit = "m"
    print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\t\tFinished {max_msgs} messages. [{duration:.1f}{unit}]')


# ─────────────────────────────────────────────
# CLI Setup
# ─────────────────────────────────────────────

parser = argparse.ArgumentParser(
    description="TBot - Telegram Bot API multi-tool. Fight phishing bots & remotely control Telegram bots.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
COMMANDS:

  Reconnaissance:
    recon             Full recon (bot info + webhook status)
    read              Read incoming messages (getUpdates)
    monitor           Live-stream incoming messages (polling loop)
    chat-info         Get detailed chat info
    admins            List chat administrators
    member-count      Get chat member count
    get-member        Get info about a specific user in chat
    get-webhook       View current webhook config
    get-file          Get download URL for a file

  Actions:
    send              Send a message to a chat
    forward           Forward a message between chats
    delete-msg        Delete a message
    ban               Ban a user from a chat
    unban             Unban a user
    pin               Pin a message
    unpin             Unpin a message
    leave             Make the bot leave a chat

  Webhook Control:
    set-webhook       Set/hijack webhook URL
    delete-webhook    Remove webhook (enables getUpdates)

  Chat Admin:
    set-title         Change chat title
    set-description   Change chat description
    export-invite     Export chat invite link

  Advanced:
    raw               Call any raw Telegram Bot API method
    logout            Log out bot (10 min cooldown)
    spam              Original TBot phisher payback spam

EXAMPLES:
  python3 tbot.py --bot-id BOT_ID --token TOKEN recon
  python3 tbot.py --bot-id BOT_ID --token TOKEN read
  python3 tbot.py --bot-id BOT_ID --token TOKEN monitor
  python3 tbot.py --bot-id BOT_ID --token TOKEN admins --chat-id -123456
  python3 tbot.py --bot-id BOT_ID --token TOKEN send --chat-id -123456 --text "hello"
  python3 tbot.py --bot-id BOT_ID --token TOKEN delete-webhook
  python3 tbot.py --bot-id BOT_ID --token TOKEN set-webhook --url https://yourserver.com/hook
  python3 tbot.py --bot-id BOT_ID --token TOKEN spam --chat-id 123456 --messages 100
  python3 tbot.py --bot-id BOT_ID --token TOKEN raw --method getMe
  python3 tbot.py --bot-id BOT_ID --token TOKEN raw --method sendMessage --params '{"chat_id":"-123","text":"hi"}'
"""
)

# Global args
parser.add_argument('--bot-id', type=str, help="Bot ID", required=True)
parser.add_argument('--token', type=str, help="Bot token", required=True)
parser.add_argument('--proxy', type=str, help="Proxy address", required=False)
parser.add_argument('--proxy-port', type=int, help="Proxy port", required=False)

subparsers = parser.add_subparsers(dest='command', help='Command to run (use -h after command for details)')

# ── recon ──
subparsers.add_parser('recon', help='Get bot info + webhook status')

# ── read ──
sp_read = subparsers.add_parser('read', help='Read incoming messages (getUpdates)')
sp_read.add_argument('--limit', type=int, default=100, help='Max updates to fetch, 1-100 (default: 100)')
sp_read.add_argument('--timeout', type=int, default=0, help='Long polling timeout in seconds (default: 0)')
sp_read.add_argument('--offset', type=int, default=None, help='Update offset (to skip already-seen updates)')

# ── monitor ──
sp_monitor = subparsers.add_parser('monitor', help='Continuously poll for new messages (Ctrl+C to stop)')
sp_monitor.add_argument('--interval', type=int, default=2, help='Poll interval in seconds (default: 2)')

# ── chat-info ──
sp_chatinfo = subparsers.add_parser('chat-info', help='Get full chat info (getChat)')
sp_chatinfo.add_argument('--chat-id', type=str, required=True, help='Chat ID')

# ── admins ──
sp_admins = subparsers.add_parser('admins', help='List chat administrators')
sp_admins.add_argument('--chat-id', type=str, required=True, help='Chat ID')

# ── member-count ──
sp_mcount = subparsers.add_parser('member-count', help='Get chat member count')
sp_mcount.add_argument('--chat-id', type=str, required=True, help='Chat ID')

# ── get-member ──
sp_gmember = subparsers.add_parser('get-member', help='Get info about a specific chat member')
sp_gmember.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_gmember.add_argument('--user-id', type=int, required=True, help='User ID')

# ── send ──
sp_send = subparsers.add_parser('send', help='Send a message to a chat')
sp_send.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_send.add_argument('--text', type=str, required=True, help='Message text')
sp_send.add_argument('--parse-mode', type=str, choices=['HTML', 'Markdown', 'MarkdownV2'], help='Parse mode')
sp_send.add_argument('--silent', action='store_true', help='Send without notification')

# ── delete-msg ──
sp_delmsg = subparsers.add_parser('delete-msg', help='Delete a message')
sp_delmsg.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_delmsg.add_argument('--message-id', type=int, required=True, help='Message ID to delete')

# ── forward ──
sp_fwd = subparsers.add_parser('forward', help='Forward a message between chats')
sp_fwd.add_argument('--from-chat-id', type=str, required=True, help='Source chat ID')
sp_fwd.add_argument('--to-chat-id', type=str, required=True, help='Destination chat ID')
sp_fwd.add_argument('--message-id', type=int, required=True, help='Message ID to forward')

# ── get-webhook ──
subparsers.add_parser('get-webhook', help='Get current webhook info (JSON)')

# ── delete-webhook ──
sp_dwh = subparsers.add_parser('delete-webhook', help='Remove webhook (enables getUpdates)')
sp_dwh.add_argument('--drop-pending', action='store_true', help='Drop all pending updates too')

# ── set-webhook ──
sp_swh = subparsers.add_parser('set-webhook', help='Set/hijack webhook URL')
sp_swh.add_argument('--url', type=str, required=True, help='Webhook URL (HTTPS)')
sp_swh.add_argument('--secret-token', type=str, help='Secret token for verification header')

# ── ban ──
sp_ban = subparsers.add_parser('ban', help='Ban a user from chat')
sp_ban.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_ban.add_argument('--user-id', type=int, required=True, help='User ID to ban')

# ── unban ──
sp_unban = subparsers.add_parser('unban', help='Unban a user from chat')
sp_unban.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_unban.add_argument('--user-id', type=int, required=True, help='User ID to unban')

# ── pin ──
sp_pin = subparsers.add_parser('pin', help='Pin a message in chat')
sp_pin.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_pin.add_argument('--message-id', type=int, required=True, help='Message ID to pin')
sp_pin.add_argument('--silent', action='store_true', help='Pin without notification')

# ── unpin ──
sp_unpin = subparsers.add_parser('unpin', help='Unpin a message')
sp_unpin.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_unpin.add_argument('--message-id', type=int, default=None, help='Message ID (latest if omitted)')

# ── leave ──
sp_leave = subparsers.add_parser('leave', help='Make the bot leave a chat')
sp_leave.add_argument('--chat-id', type=str, required=True, help='Chat ID')

# ── set-title ──
sp_title = subparsers.add_parser('set-title', help='Set chat title (admin required)')
sp_title.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_title.add_argument('--title', type=str, required=True, help='New title')

# ── set-description ──
sp_desc = subparsers.add_parser('set-description', help='Set chat description (admin required)')
sp_desc.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_desc.add_argument('--description', type=str, required=True, help='New description')

# ── export-invite ──
sp_invite = subparsers.add_parser('export-invite', help='Export chat invite link')
sp_invite.add_argument('--chat-id', type=str, required=True, help='Chat ID')

# ── get-file ──
sp_getfile = subparsers.add_parser('get-file', help='Get file download URL from file_id')
sp_getfile.add_argument('--file-id', type=str, required=True, help='File ID (from message attachments)')

# ── logout ──
subparsers.add_parser('logout', help='Log out bot from cloud API (10 min cooldown)')

# ── raw ──
sp_raw = subparsers.add_parser('raw', help='Call any raw Telegram Bot API method')
sp_raw.add_argument('--method', type=str, required=True, help='API method name (e.g. getMe, sendMessage)')
sp_raw.add_argument('--params', type=str, default=None, help='JSON params string, e.g. \'{"chat_id": "-123"}\'')

# ── spam (original functionality) ──
sp_spam = subparsers.add_parser('spam', help='Original TBot phisher payback spam')
sp_spam.add_argument('--chat-id', type=str, required=True, help='Chat ID')
sp_spam.add_argument('--messages', type=int, default=1, help='Amount of messages (default: 1)')
sp_spam.add_argument('--text', type=str, default=None, help='Custom message (use P_IP, P_EMAIL, P_PASSWORD, P_ZIP, P_CITY, P_RANDHIGHINT, P_ORG)')
sp_spam.add_argument('--min-sleep', type=int, default=1, help='Min sleep between messages (default: 1)')
sp_spam.add_argument('--max-sleep', type=int, default=4, help='Max sleep between messages (default: 4)')
sp_spam.add_argument('--disable-check', action='store_true', help='Skip connectivity check')
sp_spam.add_argument('--name-list', type=str, default=None, help='First names wordlist path (optional)')
sp_spam.add_argument('--surname-list', type=str, default=None, help='Last names wordlist path (optional)')
sp_spam.add_argument('--domain-list', type=str, default=None, help='Domains wordlist path (optional)')
sp_spam.add_argument('--city-list', type=str, default=None, help='Cities wordlist path (optional)')


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

args = parser.parse_args()

if not args.command:
    parser.print_help()
    sys.exit(0)

# Build proxy and API client
proxy = build_proxy(args.proxy, args.proxy_port)
api = TelegramAPI(args.bot_id, args.token, proxy)

# Route to command handler
command_map = {
    'recon':            cmd_recon,
    'read':             cmd_read,
    'monitor':          cmd_monitor,
    'chat-info':        cmd_chat_info,
    'admins':           cmd_admins,
    'member-count':     cmd_member_count,
    'get-member':       cmd_get_member,
    'send':             cmd_send,
    'delete-msg':       cmd_delete_msg,
    'forward':          cmd_forward,
    'get-webhook':      cmd_get_webhook,
    'delete-webhook':   cmd_delete_webhook,
    'set-webhook':      cmd_set_webhook,
    'ban':              cmd_ban,
    'unban':            cmd_unban,
    'pin':              cmd_pin,
    'unpin':            cmd_unpin,
    'leave':            cmd_leave,
    'set-title':        cmd_set_title,
    'set-description':  cmd_set_description,
    'export-invite':    cmd_export_invite,
    'get-file':         cmd_get_file,
    'logout':           cmd_logout,
    'raw':              cmd_raw,
    'spam':             cmd_spam,
}

handler = command_map.get(args.command)
if handler:
    if args.command == 'spam' and not args.disable_check:
        try:
            r = requests.get('https://api.ipify.org', proxies=proxy, timeout=10)
            if r.ok:
                print(f'Public IP: {r.text}')
                time.sleep(2)
            else:
                print('No connection! Use --disable-check to skip.')
                sys.exit(0)
        except Exception:
            print('No connection! Use --disable-check to skip.')
            sys.exit(0)
    handler(api, args)
else:
    print(f"[!] Unknown command: {args.command}")
    parser.print_help()
