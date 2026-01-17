# Notas

## Seguridad
Se crea una VPC con plantillas de aws que tiene una subred pública para ubicar servicios que necesitan acceso a internet y subred privada para la capa de persistencia de datos.

![VPC 0](images/VPC_00.png)
![VPC 1](images/VPC_01.png)


Nota: algunos servicios son globales (kinesis, lambda) realmente no se les asocia VPC.

## EC2 
Este componente iaas lo ubicaremos en la subred pública para que sea accesible vía internet por la recolección de datos y por los usuarios que quieran ver el dashboard.
Idealmente deberían ser EC2´s diferentes pero para la práctica utilizaremos la misma.

![EC2 0](images/EC2_00.png)
![EC2 1](images/EC2_01.png)
![EC2 2](images/EC2_02.png)
![EC2 3](images/EC2_03.png)
![EC2 SEC](images/EC2_SEC1.png)


Descarga ppk para putty
Nota: la ip es dinámica, al reinciar cambia.

### Script setup
Instalamos websoclet-client/boto3 para producer y flask para app web test
```bash
#!/bin/bash
sudo dnf update -y
sudo dnf install -y python3 python3-pip
pip install websocket-client
pip install flask boto3
dnf install -y httpd
systemctl enable httpd
systemctl start httpd
```

```bash
login as: ec2-user
Authenticating with public key "ec2-bigdata-2"
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
    ~~~         /
      ~~._.   _/
         _/ _/
       _/m/'
Last login: Sat Jan 17 10:39:59 2026 from 159.147.237.164
[ec2-user@ip-10-0-0-9 ~]$ pwd
/home/ec2-user
[ec2-user@ip-10-0-0-9 ~]$ ls -ltr
total 0
drwxr-xr-x. 3 ec2-user ec2-user 59 Jan 16 23:39 bigdata
[ec2-user@ip-10-0-0-9 ~]$ ls -l bigdata
total 8
-rw-r--r--. 1 ec2-user ec2-user 893 Jan 16 23:09 producer.py
drwxr-xr-x. 2 ec2-user ec2-user  24 Jan 16 23:42 templates
-rw-r--r--. 1 ec2-user ec2-user 739 Jan 16 23:35 webapp.py
[ec2-user@ip-10-0-0-9 ~]$ ls -l bigdata/templates/
total 4
-rw-r--r--. 1 ec2-user ec2-user 618 Jan 16 23:42 index.html
[ec2-user@ip-10-0-0-9 ~]$
```

## Kinesis streams
Servicio tipo cola dónde guardaremos los eventos enviados por la recolección.

### Setup
![KIN 0](images/KINESIS_00.png)
![KIN 1](images/KINESIS_01.png)
![KIN 2](images/KINESIS_02.png)

## Lambda

### Setup
![LAMBDA_01](images/LAMBDA_01.png)
![LAMBDA_02](images/LAMBDA_02.png)
![LAMBDA_03](images/LAMBDA_03.png)

## DynamoDB

### Setup
![DYN_00](images/DYNAMO_00.png)

## Webapp
### Start
![WEBAPP_00](images/WEBAPP_00.png)

## Unit Test / Demo

```
Entrada:
	
{"data":[{"c":null,"p":95372.09,"s":"BINANCE:BTCUSDT","t":1768655932976,"v":0.00063},{"c":null,"p":95372.09,"s":"BINANCE:BTCUSDT","t":1768655933296,"v":0.00058}],"type":"trade"}


DynamoDB:
{
  "pair": {
    "S": "BINANCE:BTCUSDT"
  },
  "wtime": {
    "S": "1768655880"
  },
  "last_price": {
    "N": "95372.09"
  },
  "trades": {
    "N": "2"
  },
  "ttl": {
    "N": "1768659480"
  },
  "volume": {
    "N": "0.00121"
  }
}	

webapp:

BINANCE:BTCUSDT | Price: 95372.09 | Volume: 0.00121 | Trades: 2
```

* Estado inicial:

![UT 0](images/UNIT_TEST_00.png)

* Producimos 1 evento:

![UT 1](images/UNIT_TEST_01.png)

* Comprobamos paso por kinesis:

![UT 2](images/UNIT_TEST_02.png)

* Comprobamos paso por lambda:

![UT 3](images/UNIT_TEST_03.png)

* Comprobamos persistencia DynamoDB:

![UT 4](images/UNIT_TEST_04.png)

* Webapp:

![UT 5](images/UNIT_TEST_05.png)


# Master layer / flujo validación
### Sink S3
Dentro del mismo producer añadirmos un push a S3 que nos servirá para tener la capa de datos **maestra** que podemos utilizar para validar y consolidar datos al final del día por ejemplo. Esta capa también se podría utilizar con fines más analíticos.

### Lambda RDS


# Otros

## Acceso ssh Putty


