from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'devil in the sky'
DB_NAME = 'bmat'

# DATABASE = MongoClient("mongodb://ant-login7.linux.crg.es:27017")[DB_NAME]
DATABASE = MongoClient()[DB_NAME]
EPG = DATABASE.epg
MUSIC = DATABASE.music
CHANNELS = DATABASE.channels

CSV = set(['csv', 'txt'])

DEBUG = True
PROPAGATE_EXCEPTIONS = True
