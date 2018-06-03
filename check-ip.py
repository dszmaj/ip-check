import configparser
import json

import peewee
import requests

from pprint import pprint

db = peewee.SqliteDatabase('ips.db')


class IpNumbers(peewee.Model):
    service = peewee.CharField(primary_key=True)
    current_ip = peewee.CharField(null=True)
    previous_ip = peewee.CharField(null=True)

    class Meta:
        database = db


def extract_ip(service):
    parsed = json.loads(requests.get(service).text)
    return parsed['ip'] if parsed.get('ip') else parsed['origin']


if __name__ == '__main__':
    db.connect()
    db.create_tables([IpNumbers])
    
    services = [
        'https://jsonip.com/',
        'http://httpbin.org/ip',
        'https://api.ipify.org/?format=json'
    ]
    
    ips = [IpNumbers.get_or_create(service=url)[0] for url in services]
    
    for ip in ips:
        ip.previous_ip = ip.current_ip
        ip.current_ip = extract_ip(ip.service)
        ip.save()

    config = configparser.ConfigParser()
    config.read('.env')

    r = requests.post(
        config['emaillabs']['API'],
        auth=(
            config['emaillabs']['KEY'],
            config['emaillabs']['SECRET']
        ),
        json={
            'to': [
                config['smtp']['RECEPIENT'],
            ],
            'smtp_account': config['emaillabs']['ACCOUNT'],
            'subject': 'Nowy adres IP koparki',
            'text': 'abcd',
            'from': config['smtp']['SENDER']
        }
    )
    
    pprint(r.content.decode())
