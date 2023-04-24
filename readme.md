## TBOT

# Reason
TBOT is made, to stop phish campaigns - which are using a Telegram bot as exfiltration destination. TBOT generates random messages, which suppose to flood the phishers mailbox. As soon as the phishers kicks out the used bot (and its token), the current phish campaign is useless and disarmed.

# Requirements 

```shell
pip3 install requests
pip3 install pathlib
```

All other needed libraries are Python default.

# Usage

For an overview of all functions, use the `-h` parameter.
```
python3 tbot.py -h
```

The required params are:
```
python3 tbot.py --bot-id <bot-id> --token <token> --chat-id <chat-id>
```
# All functions
```
 -h, --help            show this help message and exit
  --bot-id BOT_ID       ID of telegram bot
  --token TOKEN         Token of telegram bot
  --chat-id CHAT_ID     Chat ID
  --messages MESSAGES   Amount of messages
  --text TEXT           Define own message to send. Will be url encoded. Use variables inside to make it random: P_IP|P_EMAIL|P_PASSWORD|P_ZIP|P_CITY|P_RANDHIGHINT|P_ORG
  --min-sleep MIN_SLEEP
                        Min sleep time between messages
  --max-sleep MAX_SLEEP
                        Max sleep time between messages
  --disable-check       Disable connectivity check
  --name-list NAME_LIST
                        First Names Wordlist
  --surname-list SURNAME_LIST
                        Last Names Wordlist
  --domain-list DOMAIN_LIST
                        Domains Wordlist
  --city-list CITY_LIST
                        City Wordlist
```
