import os
import sys
import time
import requests
import random
import string
import pathlib
import argparse
import urllib.parse
from datetime import datetime


header = """
_________ ______   _______ _________
\__   __/(  ___ \ (  ___  )\__   __/
   ) (   | (   ) )| (   ) |   ) (   
   | |   | (__/ / | |   | |   | |   
   | |   |  __ (  | |   | |   | |   
   | |   | (  \ \ | |   | |   | |   
   | |   | )___) )| (___) |   | |   
   )_(   |/ \___/ (_______)   )_(   
                                    
"""
print(header)

def get_list(path):
    wordlist = []
    with open(path, "r") as f:
        for line in f.readlines():
            wordlist.append(line.replace('\n',''))
    return wordlist

def random_pw(s=8, e=12):
    n = random.randint(s,e)
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=n))

def random_email(name, family_name, domain_list):
    return f'{random.choice(name).lower()}.{random.choice(family_name).lower()}@{random.choice(domain_list)}'

def send_message(msg):
    url = base_url + bot_id + ":" + token + "/sendMessage?chat_id=-" + chat_id + f"&text={msg}"
    r = requests.get(url)
    if r.ok:
        return r.status_code
    else:
        return r.status_code

def create_msg(text=None):
    P_EMAIL = random_email(name_list,family_name_list, domain_list)
    P_PASSWORD = random_pw()
    P_IP = f"{random.randint(11,230)}.{random.randint(11,230)}.{random.randint(11,230)}.{random.randint(11,230)}"
    P_ZIP = random.randint(1000,88999)
    P_COUNTRYCODE = "".join(random.choices(string.ascii_uppercase) + random.choices(string.ascii_uppercase))
    P_CITY = random.choice(city_list)
    P_RANDHIGHINT = str(random.randint(20000000,22000000))
    P_ORG = random.choice(family_name_list) + "-" + random.choice(family_name_list)
    

    default = """<b>OFFICE365-HTML-LOGS@ZERO</b>
    [1] 24/04/2023
    <b>USER-AGENT: </b>Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/P_RANDHIGHINT Firefox/105.0
    <a>seemee: @pwned</a>
    <b>EMAIL: </b><pre>P_EMAIL</pre>
    <b>PASSWORD: </b><a>P_PASSWORD</a>
    <b>Location: </b>IP: P_IP | CITY: P_CITY | COUNTRY: P_COUNTRYCODE | ORG: P_ORG | POSTAL: P_ZIP&parse_mode=html HTTP/2"""

    if text is None:
        text = default

    text = text.replace('P_EMAIL', P_EMAIL).replace('P_PASSWORD', P_PASSWORD).replace('P_IP', P_IP).replace('P_ZIP', str(P_ZIP)).replace('P_COUNTRYCODE', P_COUNTRYCODE).replace('P_CITY', P_CITY).replace('P_RANDHIGHINT', P_RANDHIGHINT).replace("P_ORG", P_ORG)


    text = urllib.parse.quote_plus(text)
    
    return text, P_EMAIL


parser = argparse.ArgumentParser(description="This bot is made to fight against telegram phishing bots. It will does that with sending many randomized messages. Goal is it, that the phisher kicks out the bot and disables the used token with it.")
parser.add_argument('--bot-id', type=str, help="ID of telegram bot", required=True)
parser.add_argument('--token', type=str, help="Token of telegram bot", required=True)
parser.add_argument('--chat-id', type=str, help="Chat ID", required=True)
parser.add_argument('--messages', type=int, help="Amount of messages", default=1, required=False)
parser.add_argument('--text', type=str, help="Define own message to send. Will be url encoded. Use variables inside to make it random: P_IP|_EMAIL|P_PASSWORD|P_ZIP|P_CITY|P_RANDHIGHINT|P_ORG", required=False, default=None)
parser.add_argument('--min-sleep', type=int, help="Min sleep time between messages", default=1, required=False)
parser.add_argument('--max-sleep', type=int, help="Max sleep time between messages", default=4, required=False)
parser.add_argument('--disable-check', help="Disable connectivity check", required=False, action='store_true')
parser.add_argument('--name-list', type=str, default='/usr/share/wordlists/SecLists/Usernames/Names/names.txt', help="First Names Wordlist")
parser.add_argument('--surname-list', type=str, default='/usr/share/wordlists/SecLists/Usernames/Names/familynames-usa-top1000.txt', help="First Names Wordlist")
parser.add_argument('--domain-list', type=str, default='/usr/share/wordlists/email_provider.txt', help="Domains Wordlist")
parser.add_argument('--city-list', type=str, default='/usr/share/wordlists/SecLists/Usernames/Names/names.txt', help="City Wordlist")

args = parser.parse_args()
base_url = "https://api.telegram.org/bot"
bot_id = args.bot_id
token = args.token
chat_id = args.chat_id
max_msgs = args.messages

if not args.disable_check:
    # ip check 
    r = requests.get('https://api.ipify.org')
    if r.ok:
        print(f'The public IP address which is used: {r.text}')
        print('...')
        time.sleep(5)
    else:
        print('No Connection! Please check your internet connection. Ignore connectivity test with: --disable-check')
        sys.exit(0)

if not os.path.isfile(args.name_list):
    print(f'Please define wordlist path for: --name-list')
    sys.exit(0)
if not os.path.isfile(args.surname_list):
    print(f'Please define wordlist path for: --surname-list')
    sys.exit(0)
if not os.path.isfile(args.domain_list):
    print(f'Please define wordlist path for: --domain-list')
    sys.exit(0)
if not os.path.isfile(args.city_list):
    print(f'Please define wordlist path for: --city-list')
    sys.exit(0)

print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\t\tStarting phishers paypack..')
name_list_path = pathlib.Path(args.name_list)
family_name_list_path = pathlib.Path(args.surname_list)
domain_list_path = pathlib.Path(args.domain_list)
city_list_path = pathlib.Path(args.city_list)
name_list = get_list(name_list_path)
family_name_list = get_list(family_name_list_path)
city_list = get_list(city_list_path)
domain_list = get_list(domain_list_path)
start = time.time()

for i in range(max_msgs):
    txt, email = create_msg(args.text)
    ret = send_message(txt)
    time.sleep(random.randint(args.min_sleep, args.max_sleep))
    print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\t{ret}\tSending {i}/{max_msgs} [{email}]')
    if ret > 400:
        end = time.time()
        duration = end - start
        unit = "s"
        if duration >=60:
            duration = duration / 60
            unit = "m"
        elif duration >=3600:
            duration = duration / 60 / 60
            unit = "h"
        print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\tBot disabled after {i} messages. [{duration}{unit}]')
        sys.exit(0)

end = time.time()
duration = end - start
unit = "s"
if duration >=60:
    duration = duration / 60
    unit = "m"
elif duration >=3600:
    duration = duration / 60 / 60
    unit = "h"
print(f'{datetime.now().strftime("%y/%m/%d %H:%M:%S")}\tBot still active after {i} messages. [{duration}{unit}]')
sys.exit(0)   
