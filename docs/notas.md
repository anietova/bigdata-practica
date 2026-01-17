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
Last login: Fri Jan 16 23:41:02 2026 from 159.147.237.164
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

### Script setup

## Lambda

