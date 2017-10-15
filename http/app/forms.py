# -*- coding: UTF-8 -*-
from app import app
from flask import request, flash
from flask_wtf import Form
from flask_admin.form.upload import FileUploadField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename


def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    return secure_filename('file-%s%s' % parts)


class ClientForm(Form):
    tbl = FileUploadField('File', namegen=prefix_name, validators=[DataRequired()])
