# [ec2-user@ip-10-0-0-9 bigdata]$ cat producer.py
token="removed"

import websocket
import json
import boto3

import time
import uuid

kinesis = boto3.client("kinesis", region_name="us-east-1")

s3 = boto3.client("s3", region_name="us-east-1")
S3_BUCKET = "raw-bucket-grupo20"
S3_PREFIX = "raw/trades/"

def on_message(ws, message):
    print(message)
    data = json.loads(message)

    # envío kinesis
    kinesis.put_record(
        StreamName='bc-data',
        Data=json.dumps(data),
        PartitionKey="1"
    )
    
    # sink s3
    key = f"{S3_PREFIX}trade_{int(time.time() * 1000)}_{uuid.uuid4()}.json"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )

    # prueba unitaria
    # ws.close()

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
