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
![image](https://user-images.githubusercontent.com/73298827/234122669-ab223fa9-56b8-477e-8d2b-c96c3995b9c3.png)

The required params are:
```
python3 tbot.py --bot-id <bot-id> --token <token> --chat-id <chat-id>
```


Using TBOT is quite simple. 
