# FTX Order Notifier for Telegram

You can send message to any Telegram chat/group/channel when you do new order on FTX using this script.

## Requirements

* Python 3.9
* Pip 21

## Installation

* Set FTX API authentication variables in [bot.py](bot.py) file; 
    - Line 9: `ftx_api_key`.
    - Line 10: `ftx_api_secret`.
* Set Telegram variables; 
    - Line 11: `telegram_bot_api_key`.
    - Line 12: `telegram_chat_id`.
* Change order notifier paths; 
    - Line 2: [order-notifier.sh](order-notifier.sh).
    - Line 9 and 10: [order-notifier.service](order-notifier.service).
* Change systemd service variables; 
    - Line 5: [order-notifier.service](order-notifier.service). // User
    - Line 6: [order-notifier.service](order-notifier.service). // Group
* Install and run; 
    - `$ pip3 install -r requirements.txt`
    - `$ sudo cp order-notifier.service /etc/systemd/system/order-notifier.service`
    - `$ chmod +x order-notifier.sh`
    - `$ sudo systemctl daemon-reload`
    - `$ systemctl start order-notifier.service`

## Debug/Development

If you want to improve this script and yo run this script on your local, set `env` variable as `dev` in [bot.py](bot.py) line 8.

---

Omer Citak - 2k21
