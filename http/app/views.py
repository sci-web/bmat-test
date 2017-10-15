from app import app
from flask import request, redirect, render_template, url_for, flash, Response
import datetime
import os
from itertools import chain
from .forms import ClientForm
from .model import DB


@app.route('/')
def index():
    form = ClientForm()
    return render_template('index.html', form=form)


def extension_ok(filename, ff):
    """ return whether file's extension is ok or not"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config[ff]


def packed(val_dict):
    # vls = ", ".join(['{}={}'.format(k, v) for k, v in val_dict.iteritems()])
    ll = []
    for k, v in val_dict.iteritems():
        exec(k + " = v")
        ll.append(k)
    return ll


@app.route('/report', methods=['GET', 'POST'])
def report():
    form = ClientForm(request.values)
    items = {}
    if request.method == 'POST':
        if form.data:
            f = request.files['catalogue']
            if f and extension_ok(f.filename, 'CSV'):
                content = f.stream.read()
                lines = content.split("\n")[1:]
                titles = content.split("\n")[0].split("\t")
                if len(titles) == 3:
                    for l in lines:
                        try:
                            title1, title2, released = l.split("\t")
                            title1 = title1.decode('cp1252').encode('utf-8').title()
                            title2 = title2.decode('cp1252').encode('utf-8').title()
                            item = DB().get_epg_data_search(title1 + title2, released)
                            items = [x for x in chain(items, item)]
                        except: 
                            print "file formating minor errors?"
                else:
                    flash("Something wrong with your file format (not TAB separated csv?)", category='error')
            else:
                flash("Something wrong with your file", category='error')
        else:
            flash("Cannot process your form: no data", category='error')
    else:
        flash("Form was not properly sent", category='error')
    channels = channels_names()
    start = datetime.datetime.strptime("2016-11-04 00:00:00", '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime("2016-11-14 23:59:59", '%Y-%m-%d %H:%M:%S')        
    return render_template('report.html', items=items, channels=channels, start=start, end=end)


@app.route('/mus_report', methods=['GET', 'POST'])
def mus_report():
    start = datetime.datetime.strptime("2016-11-04 00:00:00", '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime("2016-11-14 23:59:59", '%Y-%m-%d %H:%M:%S')
    items = DB().get_music_data(start, end)
    channels = channels_names()
    return render_template('mus_report.html', items=items, channels=channels, start=start, end=end)

def channels_names():
    names = {}
    for entry in DB().get_channel_names():
        names[entry["channel_id"]] = entry["name"]
    return names