import json
import peewee
import requests

db = peewee.SqliteDatabase('ips.db')


class IpNumbers(peewee.Model):
    service = peewee.CharField()
    ip = peewee.CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([IpNumbers])

    ips = [
        IpNumbers(
            service='http://ip.42.pl/raw',
            ip=requests.get('http://ip.42.pl/raw').content.decode()
        ),
        IpNumbers(
            service='https://jsonip.com/',
            ip=json.loads(requests.get('https://jsonip.com/').content).pop('ip')
        ),
        IpNumbers(
            service='http://httpbin.org/ip',
            ip=json.loads(requests.get('http://httpbin.org/ip').content).pop('origin')
        ),
        IpNumbers(
            service='https://api.ipify.org/?format=json',
            ip=json.loads(requests.get('https://api.ipify.org/?format=json').content).pop('ip')
        ),
    ]
    
    for ip in ips:
        ip.save()
