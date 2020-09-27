from flask import Flask, Blueprint, jsonify, json, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, TextField, HiddenField
from wtforms.fields.html5 import URLField, TimeField, DecimalField, IntegerField, IntegerRangeField
from wtforms.validators import DataRequired, Email, URL, NumberRange, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_bootstrap import Bootstrap
from datetime import datetime

import os
import threading
from werkzeug.utils import secure_filename
from someScript import doFile, doURL, doFileTime, doURLTime
from DFM_dm import findUsrInQueue, getAllInQueue


class QItem:
    index =  TextField(u'Idex')
    title = TextField(u'Title')
    celeb = TextField(u'Celeb')
    vid = TextField(u'video')
    usr = TextField(u'User')

    def __init__(self, i, t, v, c, u):
        self.index = i
        self.title = t
        self.celeb = c
        self.vid = v
        self.usr = u


admin_part = Blueprint('admin_part', __name__, template_folder='templates')


@admin_part.route('/admin')
def daminView():
    # jsonify(getAllInQueue()
    print('>>>> ')
    q = []
    allInQ = getAllInQueue()
    #for it in getAllInQueue():
    i = 0
    while i < len(allInQ):
        it = allInQ[i]
        q.append(QItem(i, it[0], it[1], it[2], it[3]))
        print( it[0])
        print( it[1])
        print( it[2])
        print( it[3])
        i+=1

    return render_template('admin.html', items=q)
