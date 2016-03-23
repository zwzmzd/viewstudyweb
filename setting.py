# coding: utf-8
import os

ratetype=0
ABSDIR = os.path.dirname(os.path.abspath(__file__))

#数据库设定
try:
    DB = {
        'user': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
        'password': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
        'name': os.environ['OPENSHIFT_APP_NAME'],
        'host': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
        'port': os.environ['OPENSHIFT_MYSQL_DB_PORT']
    }
    debug = True
    entry_token = '0xffd'
except:
    DB = {
        'user': 'root',
        'password': 'toor',
        'host': 'localhost',
        'port': '3306',
        'name': 'goodview'
    }
    debug = True
    entry_token = '0xffd'
