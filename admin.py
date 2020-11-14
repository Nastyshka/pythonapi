from flask import Flask, Blueprint, jsonify, json, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, TextField, HiddenField
from wtforms.fields.html5 import URLField, TimeField, DecimalField, IntegerField, IntegerRangeField,IntegerField
from wtforms.validators import DataRequired, Email, URL, NumberRange, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_bootstrap import Bootstrap
from datetime import datetime

import os
import threading
import ast
from werkzeug.utils import secure_filename
from someScript import doFile, doURL, doFileTime, doURLTime
from DFM_dm import findUsrInQueue, getAllInQueue, deleteFromQueue, editQueueLine, celebs, getCelebs, STATE_CHOISES, sortSheetData, getTags

CELEB_CHOISES = getCelebs()
TAG_CHOISES = getTags()
class QItem (FlaskForm):
    index = IntegerField(u'Idex')
    title = TextAreaField(u'Title')
    celeb = SelectField(u'Celeb', choices=CELEB_CHOISES)
    vid = TextField(u'video')
    usr = TextField(u'User')
    state = SelectField(u'State', choices=STATE_CHOISES)
    tags = SelectMultipleField(u'State', choices=TAG_CHOISES)

admin_part = Blueprint('admin_part', __name__, template_folder='templates')


@admin_part.route('/sort')
def sort ():
    sortSheetData()


@admin_part.route('/admin')
def daminView():   
    print('>>>> admin >')
    q = []
    allInQ = getAllInQueue()
    i = 0
    while i < len(allInQ):
        it = allInQ[i]
        qi = QItem()
        qi.index.data = i+1
        qi.title.data = it[0]

        qi.celeb.data = it[2]
        qi.vid.data = it[1]
        qi.usr = it[3]
        qi.state.data = it[4]
        

        if (len(it[5]) > 0):
            qi.tags.data = ast.literal_eval(it[5])


        if (len(it) > 6) :
            qi.resUrl = it[6]
        q.append(qi)
        i+=1

    return render_template('admin.html', items=q)

@admin_part.route('/deleteLine/<ind>', methods=['GET', 'POST'])
def deleteLine(ind):
    print('>>>> delete line > ')
    print(ind)
    deleteFromQueue(int(ind))
    return redirect(url_for('admin_part.daminView'))

@admin_part.route('/editLine', methods = ['POST'])
def editLine (): 
    form = QItem()
    print ('>>>>> edit line >')
    print ('>>>>>' + form.title.data)
    print ('>>>>>' + form.celeb.data)
    rowData = []
    rowData.append(form.title.data)
    rowData.append(form.vid.data)
    rowData.append(form.celeb.data)
    rowData.append(form.usr.data)
    rowData.append(form.state.data)

    ind = form.index.data
    editQueueLine(rowData, ind)
    sortSheetData()
    return redirect(url_for('admin_part.daminView'))

@admin_part.route('/queueForUsers')
def queueForUsersView():
    print('>>>> queueForUsers >')
    q = []
    allInQ = getAllInQueue()

    i = 0
    while i < len(allInQ):
        it = allInQ[i]
        qi = QItem()
        qi.index.data = i+1
        qi.title.data = it[0]

        qi.celeb.data = it[2]
        qi.vid.data = it[1]
        qi.usr = it[3]
        qi.state.data = it[4]
        qi.tags.data = it[5]

        if (len(it) > 6) :
            qi.resUrl = it[6]
        q.append(qi)
        i+=1

    return render_template('queueForUsers.html', items=q)