import base64
import json
from collections import defaultdict
from decimal import Decimal

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("trades")

WINDOW_SECONDS = 60
TTL_SECONDS = 3600

def window_start(ts_ms: int) -> int:
    ts_sec = ts_ms // 1000
    return ts_sec - (ts_sec % WINDOW_SECONDS)

def lambda_handler(event, context):
    # Tenemos que poner volumen a decimal, dynamo no se lleva bien con los floats
    aggregates = defaultdict(lambda: {
        "trades": 0,
        "volume": Decimal("0"),
        "last_price": None
    })

    for record in event["Records"]:
        payload = base64.b64decode(
            record["kinesis"]["data"]
        ).decode("utf-8")

        msg = json.loads(payload)

        if msg.get("type") != "trade":
            continue
                
        for trade in msg["data"]:
            pair = trade["s"]
            price = Decimal(str(trade["p"]))
            volume = Decimal(str(trade["v"]))
            ts = trade["t"]

            win = window_start(ts)
            key = (pair, win)

            agg = aggregates[key]
            agg["trades"] += 1
            agg["volume"] += volume
            agg["last_price"] = price


    # la clave de la tabla es compuesta por pair + window time
    for (pair, win), agg in aggregates.items():
        table.update_item(
            Key={
                "pair": pair,
                "wtime": str(win)
            },
            UpdateExpression="""
                ADD trades :t, volume :v
                SET last_price = :p,
                    #ttl = :ttl
            """,
            ExpressionAttributeValues={
                ":t": Decimal(agg["trades"]),
                ":v": agg["volume"],
                ":p": agg["last_price"],
                ":ttl": int(win + TTL_SECONDS)
            },
            ExpressionAttributeNames={
                "#ttl": "ttl"
            }
        )

