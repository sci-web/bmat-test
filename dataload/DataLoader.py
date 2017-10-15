# -*- coding: UTF-8 -*-
import datetime, time
from cookData import DBcall, readData_csv, is_match


def epg(csv):
    tbl = readData_csv(csv)
    keys = tbl[0].split("\t")
    for r in tbl[1:]:  # except 1st row which is column names
        row = r.split("\t")
        udata = {}
        day = row[4]
        day = day[0:4] + "-" + day[4:6] + "-" + day[6:8]
        dt = day + " " + row[5]
        dt = datetime.datetime.strptime(dt, '%Y-%m-%d %I:%M:%S %p')
        # print dt
        duration = time.strftime('%H:%M:%S', time.gmtime(int(row[6])))
        udata = {keys[0] : row[0], keys[6] : duration, "duration_secs" : int(row[6]), "time" : dt, keys[2] : row[2].decode('cp1252').encode('utf-8').title()}
        bdata = {"broadcast" : [udata]}
        idata = {keys[1] : row[1].decode('cp1252').encode('utf-8').title(), keys[3] : row[3]} #  look for matches only by release year & original title
        data = dict(idata, **bdata)
        if is_match('epg', idata):
            DBcall('epg').updateDatapull(idata, {"broadcast" : udata})
        else:
            DBcall('epg').loadData([data])

def music(csv):
    tbl = readData_csv(csv)
    keys = tbl[0].split("\t")
    for r in tbl[1:]:  # except 1st row which is column names
        row = r.split("\t")
        udata = {}
        dt_s = datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
        dt_e = datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
        duration = time.strftime('%H:%M:%S', time.gmtime(int(row[6])))
        query = {"broadcast.channel_id": row[0]}
        program = {}
        for entry in DBcall('epg').findDatalist(query):
            for b in entry["broadcast"]:
                if b["channel_id"] == row[0] and b["time"] + datetime.timedelta(seconds=b["duration_secs"]) > dt_e and b["time"] < dt_s:
                    program["work"] = entry["program_original_title"]
        udata = {keys[0] : row[0], keys[4] : dt_s, keys[5] : dt_e, keys[6] : duration}
        udata = dict(udata, **program)
        bdata = {"appeared" : [udata]}
        idata = {keys[1] : row[1].decode('cp1252').encode('utf-8'), keys[2] : row[2].decode('cp1252').encode('utf-8'), keys[3] : row[3].decode('cp1252').encode('utf-8')}
        data = dict(idata, **bdata)
        if is_match('matches', idata):
            DBcall('music').updateDatapull(idata, {"appeared" : udata})
        else:
            DBcall('music').loadData([data])

def channels(csv):
    tbl = readData_csv(csv)
    keys = tbl[0].split("\t")
    for r in tbl[1:]:  # except 1st row which is column names
        row = r.split("\t")
        data = {keys[0] : row[0], keys[1] : row[1], keys[2] : row[2].decode('cp1252').encode('utf-8')}
        DBcall('channels').loadData([data])

def main():
    epg('../csv/epg.csv')
    music('../csv/all_matches_channels.csv')
    channels('../csv/channels.csv')


if __name__ == '__main__':
    main()
