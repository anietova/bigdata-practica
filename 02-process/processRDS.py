import json
import boto3
import pymysql
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

def lambda_handler(event, context):
    
    try:
        logger.info("Evento recibido: %s", event) 
        record = event["Records"][0]

        bucket = record["s3"]["bucket"]["name"]

        key = record["s3"]["object"]["key"]


        obj = s3.get_object(Bucket=bucket, Key=key)

        body = obj["Body"].read().decode("utf-8")
        # key = "hola"
        # body = "{\"data\":[{\"c\":null,\"p\":95436.32,\"s\":\"BINANCE:BTCUSDT\",\"t\":1768671899513,\"v\":0.0002}],\"type\":\"trade\"}"
        logger.info("5: %s", event) 
        trade = json.loads(body)
        
        conn = pymysql.connect(
            host="bigdata.cqsywhot0rqe.us-east-1.rds.amazonaws.com",
            user="admin",
            password="",
            database="grupo20db",
            connect_timeout=10
        )

        for trade in trade["data"]:
            cur = conn.cursor()

            cur.execute("""
                 INSERT INTO trades
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
    except Exception as e:
        logger.error("Error en Lambda RDS: %s", e)