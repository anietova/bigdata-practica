# [ec2-user@ip-10-0-0-9 bigdata]$ cat producer.py
token="removed"

import websocket
import json
import boto3


def on_message(ws, message):
    kinesis = boto3.client('kinesis', region_name='us-east-1')
    print(message)
    data = json.loads(message)

    kinesis.put_record(
        StreamName='bc-data',
        Data=json.dumps(data),
        PartitionKey="1"
    )
    # prueba unitaria
    ws.close()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token="+token,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
