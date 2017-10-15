#!/usr/bin/python
import re, os, sys
from pymongo import MongoClient
from datetime import datetime


class DBcall(object):
    SECRET_KEY = 'devil in the sky'
    DATABASE = MongoClient()['bmat']

    def __init__(self, collection):
        self.client = self.DATABASE[collection]

    def loadData(self, data):
        for doc in data:
            try:
                self.client.insert_one(doc)
            except Exception, e:
                print "Load to DB failed: " + str(e)

    def updateDatapull(self, keys, values):
        try:
            self.client.update_one(keys, {'$addToSet': values})
        except Exception, e:
            print "Update DB record failed: " + str(e)

    def findData(self, keys):
        return self.client.find_one(keys)

    def findDatalist(self, keys):
        return self.client.find(keys)


# returns lines from file except the commented ones
def readData_csv(file):
    lines = []
    with open(file, "r") as ff:
        text = ff.read()
        rlines = text.splitlines()
        for l in rlines:
            if not re.match("^\#", l):      # data can be commented out
                nl = re.sub(r'\"', '', l)   # no quotes allowed
                if nl != "":
                    lines.append(nl)
    return lines


def is_match(coll, keys):
    if DBcall(coll).findData(keys):
        return 1
    return 0
