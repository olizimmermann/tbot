import os
import sys
import time
import requests
import random
import string
import pathlib
import urllib.parse

base_url = 'https://api.telegram.org/bot'
bot_id = ''
token = ''
chat_id = ''

name_list_path = pathlib.Path('/usr/share/wordlists/SecLists/Usernames/Names/names.txt')
family_name_list_path = pathlib.Path('/usr/share/wordlists/SecLists/Usernames/Names/familynames-usa-top1000.txt')
domain_list = ['gmail.com', 'proton.me', 'aol.com', 'email.com']
city_list_path = pathlib.Path('/usr/share/wordlists/SecLists/Miscellaneous/us-cities.txt')

def random_pw(s=8, e=12):
    n = random.randint(s,e)
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=n))

def random_email(name, family_name, domain=domain_list):
    return f'{random.choice(name).lower()}.{random.choice(family_name).lower()}@{random.choice(domain_list)}'

with open(name_list_path, "r") as f:
    name_list = []
    for line in f.readlines():
        name_list.append(line.replace('\n',''))

with open(family_name_list_path, "r") as f:
    family_name_list = []
    for line in f.readlines():
        family_name_list.append(line.replace('\n',''))

with open(city_list_path, 'r') as f:
    city_list = []
    for line in f.readlines():
        city_list.append(line.replace('\n',''))

def send_message(msg):
    url = base_url + bot_id + ":" + token + "/sendMessage?chat_id=-" + chat_id + f"&text={msg}"
    r = requests.get(url)
    if r.ok:
        return r.status_code
    else:
        return r.status_code

def create_msg():
    P_EMAIL = random_email(name_list,family_name_list)
    P_PASSWORD = random_pw()
    P_IP = f"{random.randint(11,230)}.{random.randint(11,230)}.{random.randint(11,230)}.{random.randint(11,230)}"
    P_ZIP = random.randint(1000,88999)
    P_COUNTRYCODE = "".join(random.choices(string.ascii_uppercase) + random.choices(string.ascii_uppercase))
    P_CITY = random.choice(city_list)
    P_GECKOVERSION = str(random.randint(20000000,22000000))
    P_ORG = random.choice(family_name_list) + "-" + random.choice(family_name_list)
    
    text = """<b>OFFICE365-HTML-LOGS@ZERO</b>
    [1] 19/04/2023
    <b>USER-AGENT: </b>Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/P_GECKOVERSION Firefox/105.0
    <a>seemee: @mrcew</a>
    <b>EMAIL: </b><pre>P_EMAIL</pre>
    <b>PASSWORD: </b><a>P_PASSWORD</a>
    <b>Location: </b>IP: P_IP | CITY: P_CITY | COUNTRY: P_COUNTRYCODE | ORG: P_ORG | POSTAL: P_ZIP&parse_mode=html HTTP/2"""

    text = text.replace('P_EMAIL', P_EMAIL).replace('P_PASSWORD', P_PASSWORD).replace('P_IP', P_IP).replace('P_ZIP', str(P_ZIP)).replace('P_COUNTRYCODE', P_COUNTRYCODE).replace('P_CITY', P_CITY).replace('P_GECKOVERSION', P_GECKOVERSION).replace("P_ORG", P_ORG)


    text = urllib.parse.quote_plus(text)
    
    return text, P_EMAIL

max_msgs = 100000
for i in range(max_msgs):
    txt, email = create_msg()
    ret = send_message(txt)
    time.sleep(random.randint(1,5))
    print(f'Sending {i}/{max_msgs} {ret} from {email}')
