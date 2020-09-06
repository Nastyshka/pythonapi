from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import URLField, TimeField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, URL, NumberRange, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_bootstrap import Bootstrap
from datetime import datetime
from subprocess import call

import os
import threading
from werkzeug.utils import secure_filename
from someScript import doFile, doURL, doFileTime, doURLTime


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'do not tell anyone' 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max-limit.

ALLOWED_SITES = ['porn.com', 'www.moreporn.com', 'http://localhost:5000'] #Add sites here
CELEB_CHOISES = [('Very famous lady','Very famous lady'), ('Famous lady', 'Famous lady'), ('Someone','Someone')] #Add celebrities here
VIDEO_EXT = ['WEBM', 'MP4', 'AVI', 'csv']
UPLOADS_FOLDER = 'uploads'

videoIsInProgress = False #Can upload a new video? 
lastVidStarted = datetime.now() #When tha last video processig started

#The input form
class SomeForm (FlaskForm):
    theceleb = SelectField(u'Celebrity', choices=CELEB_CHOISES)
    theURL = URLField ('theURL', validators=[Optional()])
    theStartMin = IntegerField ('Start Min', validators=[Optional(), NumberRange(min=0, max=59)])
    theStartSec = IntegerField ('Start Sec', validators=[Optional(),NumberRange(min=0, max=59)])
    theEndMin = IntegerField('End Min', validators=[Optional(),NumberRange(min=0, max=59)])
    theEndSec = IntegerField ('Start Sec', validators=[Optional(),NumberRange(min=0, max=59)])
    theFile = FileField('theFile', validators=[Optional(), FileAllowed(VIDEO_EXT, 'Bad File Type')])


@app.route('/the_form', methods=['GET', 'POST'])
def someForm():
    global videoIsInProgress
    global lastVideoStarted

    print(videoIsInProgress)
    form = SomeForm()
    if request.method == 'POST' and form.validate(): 
          if not allowed_site(form.theURL.data):
            form.theURL.errors.append("This site is not allowed") #Check allowed sites
    if form.validate_on_submit(): #If form is valid
        if form.theFile.data != None :
            #Save the video file
            res = saveTheFile(form)
            #Start processing
            threading.Thread(target=doFile(form.theceleb.data)).start()
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
        
        videoIsInProgress = True;
        lastVideoStarted  = datetime.now();
        return 'nice! {} will be ready in 5 hours'.format(form.theceleb.data)
    if (videoIsInProgress) : 
        timeLeft = datetime.now() - lastVideoStarted;
        return render_template('videoIsInProgress.html', timeToWait = timeLeft )
    else :    
        return render_template('someform.html', form=form)
    
#When the video is done you can upload a new one 
@app.route('/done')  
def videoIsDone():
    global videoIsInProgress 
    videoIsInProgress = False
    return 'Nice! the video is done'

@app.route('/')
def index():
    return render_template('home.html')
    
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

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0');

