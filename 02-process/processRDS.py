import json
import boto3
import psycopg2
import os

s3 = boto3.client("s3")

def handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read().decode("utf-8")

    trade = json.loads(body)

    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        connect_timeout=5
    )

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO raw_trades
        (pair, price, volume, trade_ts, s3_key)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        trade["s"],
        trade["p"],
        trade["v"],
        trade["t"],
        key
    ))

    conn.commit()
    cur.close()
    conn.close()
