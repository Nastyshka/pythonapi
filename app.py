from flask import Blueprint, Flask, render_template, request, redirect, url_for
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
from DFM_dm import findUsrInQueue
from admin import admin_part

app = Flask(__name__, static_folder='static')
app.register_blueprint(admin_part)
Bootstrap(app)

app.config['SECRET_KEY'] = 'do not tell anyone' 
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 10MB max-limit.

CELEB_CHOISES = [('1','Daisy Ridley'), ('2', 'Emma Stone'), ('3','Gal Gadot'), ('4', 'K AOA CHANMI'), ('5', 'Emma Watson')] #Add celebrities here
TAGS_CHOISES = [('tag 1','tag 1'), ('tag 2','tag 2'), ('tag 3','tag 3')]
ALLOWED_SITES = ['porn.com', 'www.moreporn.com', 'http://localhost:5000'] #Add sites here
VIDEO_EXT = ['WEBM', 'MP4', 'mp4', 'AVI', 'csv', 'wsdl']
# UPLOADS_FOLDER = 'C:\\DeepFun_v2\\DeepFaceLab_NVIDIA\\workspace\\newData_dst'
UPLOADS_FOLDER = 'static'

videoIsInProgress = False #Can upload a new video? 
lastVidStarted = datetime.now() #When tha last video processig started
currentProcessStep = 0
videoIsREadyToCheck = False

#The input form
class SomeForm (FlaskForm):
    theceleb = SelectField(u'Celebrity', choices=CELEB_CHOISES)
    theURL = URLField ('Video fron URL', validators=[Optional()])
    theStartMin = IntegerField ('Start Min', validators=[Optional(), NumberRange(min=0, max=59)])
    theStartSec = IntegerField ('Start Sec', validators=[Optional(),NumberRange(min=0, max=59)])
    theEndMin = IntegerField('End Min', validators=[Optional(),NumberRange(min=0, max=59)])
    theEndSec = IntegerField ('Start Sec', validators=[Optional(),NumberRange(min=0, max=59)])
    theFile = FileField('theFile', validators=[Optional(), FileAllowed(VIDEO_EXT, 'Bad File Type')])
    theDesc = TextAreaField(u'Description', validators=[Optional()])
    theTags = SelectMultipleField(u'Tags', choices=TAGS_CHOISES, validators=[Optional()])
    theUsr = HiddenField(u'Usr')
    theTitle = TextField(u'Title', validators=[Optional()])

class ResForm (FlaskForm):
    theQuality = IntegerRangeField ('Is it good? ', default=3, validators=[Optional(),NumberRange(min=0, max=5)])

@app.route('/the_form/<usr>', methods=['GET'])
@app.route('/the_form/', methods=['POST'])
def someForm(usr = '1'):
    global videoIsInProgress
    global lastVideoStarted
    global currentProcessStep

    print(videoIsInProgress)
    form = SomeForm()

    indexInQueue = findUsrInQueue(usr)
    
    if request.method == 'POST' and form.validate(): 
       
        print('>>> description > ' + form.theUsr.data)
        if not allowed_site(form.theURL.data):
            form.theURL.errors.append("This site is not allowed") #Check allowed sites
    if form.validate_on_submit(): #If form is valid
        print('>>> description > ' + form.theDesc.data)
        print(form.theTags.data)
        if form.theFile.data != None :
            #Save the video file
            res = saveTheFile(form)
            #Start processing
            
            print('>>>> save to gsheet > ' + form.theUsr.data)
            threading.Thread(target=
            doFile(
                form.theTitle.data,
                form.theceleb.data,
                str(res), 
                form.theUsr.data))
            #threading.Thread(target = doFile(form.theceleb.data)).start()
        elif form.theURL.data != None :  
            if form.theStartMin.data != None and form.theStartSec.data != None and form.theEndMin.data != None and form.theEndSec.data != None :
                #Run downloader and cutter
                threading.Thread(target=doURLTime(form.theceleb.data, form.theURL.data,form.theStartMin.data, form.theStartSec.data, form.theEndMin.data, form.theEndSec.data)).start()
                print( '>> the URL is > ' + form.theURL.data)
                print('>> cut between> {} : {} and {} : {}'.format (form.theStartMin.data, form.theStartSec.data, form.theEndMin.data, form.theEndSec.data))
            else : 
                print( '>> the ony URL is > ' + form.theURL.data)
                #Run downloader
                threading.Thread(target=doURL(form.theceleb.data, form.theURL.data)).start()
        else :
            return 'Not enough data to start'
        
        videoIsInProgress = True
        lastVideoStarted  = datetime.now()
        currentProcessStep = 1
        return 'nice! {} come back and check in 5 hours'.format(form.theceleb.data)
    #if (videoIsInProgress) : 
    if (indexInQueue >= 0) : 
        return render_template('videoIsInProgress.html', currStep = currentProcessStep, indexInQueue = indexInQueue)
    elif (videoIsREadyToCheck == True):
        return redirect(url_for('showRes', usr = usr))
    else :    
        form.theUsr.data = usr
        print( '>> the usr is > ' + form.theUsr.data)
        return render_template('someform.html', form=form)
    
@app.route('/res/<usr>', methods = ['GET', 'POST']) 
def showRes(usr = '1'):
    rform = ResForm()
    rform.resUrl = resUrl
    rform.theUsr = usr
    if rform.validate_on_submit():
        print('>>> quality ' + rform.theQuality.data )
        global videoIsREadyToCheck
        videoIsREadyToCheck = False
        return redirect(url_for('someForm'))
    return render_template('result.html', form = rform)

@app.route('/done/<vidurl>')  
def videoIsDone(vidurl=''):
    global videoIsInProgress 
    videoIsInProgress = False
    global currentProcessStep
    currentProcessStep = 0
    global videoIsREadyToCheck
    videoIsREadyToCheck = True
    if (vidurl != ''):
        global resUrl
        resUrl = siteUrl + vidurl
    
    return 'Nice! the video is done'

@app.route('/setstep/<stepNo>')
def updateCurrentStep (stepNo = 0):

    print('>>> current step is set ' + stepNo)
    global currentProcessStep
    currentProcessStep = stepNo
    return 'Current step was updated {}'.format(stepNo)

#Save the file on server    
def saveTheFile( form ):
        assets_dir = os.path.join(os.path.dirname(app.instance_path), UPLOADS_FOLDER)
        file = form.theFile.data
        filename = secure_filename(file.filename)
        file.save( os.path.join(assets_dir, filename))
        return filename

#Validate allowed sites
def allowed_site(url):
    if url == '' or url == None :
        return True
    else :
        host = url.split('/')[2].lower()
        if host in ALLOWED_SITES:
            return True
        else:
            return False

@app.route('/', methods=['GET','POST'])
def indexpage():
    return '<h1>Go to: /the_form/anyUserId instead</h1>'


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')