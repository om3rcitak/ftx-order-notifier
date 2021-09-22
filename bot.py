import websocket
import _thread
import time
import json
import hmac
import requests

env = 'prod' # dev or prod
ftx_api_key = ''
ftx_api_secret = ''
telegram_bot_api_key = ''
telegram_chat_id = ''


def on_error(ws, error):
    text = 'ATTENTION! Bot error: ' + error
    requests.get('https://api.telegram.org/bot' + telegram_bot_api_key + '/sendMessage?chat_id=' + telegram_chat_id + '&text=' + text)
    print(error)


def on_close(ws, close_status_code, close_msg):
    text = 'ATTENTION! Bot closed!'
    requests.get('https://api.telegram.org/bot' + telegram_bot_api_key + '/sendMessage?chat_id=' + telegram_chat_id + '&text=' + text)
    print("### closed ###")


def on_message(ws, message):
    data = json.loads(message)

    # print messages in dev env
    if env == 'dev':
        print(data)

    # send updates to telegram
    if data['type'] == 'update':
        if data['data']['price'] == 'None':
            data['data']['price'] = 'Position Stoped'

        text = (
            "Market: " + data['data']['market'] + "%0d%0a" +
            "Type: " + data['data']['type'] + "%0d%0a" +
            "Side: " + data['data']['side'] + "%0d%0a" +
            "Price: " + str(data['data']['price']) + "%0d%0a" +
            "Size: " + str(data['data']['size']) + "%0d%0a" +
            "Status: " + data['data']['status'] + "%0d%0a" +
            "Created At: " + data['data']['createdAt'] + "%0d%0a"
        )
        requests.get('https://api.telegram.org/bot' + telegram_bot_api_key + '/sendMessage?chat_id=' + telegram_chat_id + '&text=' + text)
        print('send: ' + data['data']['id'])


def on_open(ws):
    def run(*args):

        # send bot started message
        text = 'ATTENTION! Bot started!'
        requests.get('https://api.telegram.org/bot' + telegram_bot_api_key + '/sendMessage?chat_id=' + telegram_chat_id + '&text=' + text)

        # login
        time.sleep(1)
        ts = int(time.time() * 1000)
        data = {'op': 'login', 'args': {
            'key': ftx_api_key,
            'sign': hmac.new(ftx_api_secret.encode(), f'{ts}websocket_login'.encode(), 'sha256').hexdigest(),
            'time': ts,
        }}
        ws.send(json.dumps(data))

        # subscribe orders
        time.sleep(1)
        data = {'op': 'subscribe', 'channel': 'orders'}
        ws.send(json.dumps(data))

        # send pings
        while True:
            time.sleep(15)
            ws.send(json.dumps({'op': 'ping'}))

        # time.sleep(1)
        # ws.close()
        #print("thread terminating...")
    _thread.start_new_thread(run, ())


if env == 'dev':
    websocket.enableTrace(True)

ws = websocket.WebSocketApp("wss://ftx.com/ws/",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()
