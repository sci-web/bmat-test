# -*- coding:utf-8 -*-
from app import app
import re



class DB(object):

    def get_epg_data_search(self, title, released):
        try:
            return app.config['EPG'].find({
                '$text': {'$search': title},
                "program_release_year" : released
                }, {'score': {'$meta': 'textScore'}})
        except Exception, e:
            print e

    def get_music_data(self, start, end):
        return app.config['MUSIC'].find({ "appeared": 
                { '$elemMatch' : 
                    { "start_time": { '$gt': start }, "end_time": { '$lt': end } }
                } 
            })

    def get_channel_names(self):
        return app.config['CHANNELS'].find()
