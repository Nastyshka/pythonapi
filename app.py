from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import URLField, TimeField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, URL, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_bootstrap import Bootstrap

import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'do not tell anyone'
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/files'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max-limit.
allowed_sites = ["porn.com", "www.moreporn.com"]

CELEB_CHOISES = [('1','Very famous lady'), ('2', 'Famous lady'), ('3','Someone')]
VIDEO_EXT = ['WEBM', 'MP4', 'AVI', 'CSV']

images = UploadSet('images', IMAGES) 
configure_uploads(app, images)

class SomeForm (FlaskForm):
    theceleb = SelectField(u'Celebrity', choices=CELEB_CHOISES)
    theURL = URLField ('theURL')
    theStartMin = IntegerField ('Start Min', validators=[NumberRange(min=0, max=59)])
    theStartSec = IntegerField ('Start Sec', validators=[NumberRange(min=0, max=59)])
    theEndMin = IntegerField('End Min', validators=[NumberRange(min=0, max=59)])
    theEndSec = IntegerField ('Start Sec', validators=[NumberRange(min=0, max=59)])
    theFile = FileField('theFile', validators=[FileAllowed(VIDEO_EXT, 'Bad File Type')])


@app.route('/the_form', methods=['GET', 'POST'])
def someForm():
    form = SomeForm()
    if request.method == 'POST' and form.validate(): 
          if not allowed_site(form.theURL.data):
            form.theURL.errors.append("This site is not allowed")
    if form.validate_on_submit():
        res = saveTheFile(form)
        return 'nice! {} {}'.format(res, form.theceleb.data)
    return render_template('someform.html', form=form)
    
    
@app.route('/')
def index():
    return render_template('home.html')
    
def saveTheFile( form ):
    if form.theFile.data == None :
        return ''
    else :
        assets_dir = os.path.join(os.path.dirname(app.instance_path), 'uploads')
        file = form.theFile.data
        filename = secure_filename(file.filename)
        file.save( os.path.join(assets_dir, filename))
        return filename

def allowed_site(url):
    if url == '' or url == None :
        return True
    else :
        host = url.split('/')[2].lower()
        if host in allowed_sites:
            return True
        else:
            return False

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0');

