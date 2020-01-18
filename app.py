import warnings
warnings.filterwarnings('ignore')
from spleeter.separator import Separator
from flask import Flask,request,render_template,flash,redirect,url_for
import urllib.request
import shutil
import os
# Copy a network object to a local file
app=Flask('__main__')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        data=request.form
        url=data['url']
        downloadfile(url)
        flash("File Download Succesfully")
        return "file downloaded"
    # main()
    # makearchive('fileinzip','output/test')
    return """
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
          <ul class="flashes" style="color: red;">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}
    <form action="/" method="post">
        <input type="text" name="url">
        <input type="submit" value="Download File">

    </form>
    <a href="/split">Split File</a>
    </body>
    </html>
    """


@app.route('/split',methods=['GET','POST'])
def split():
    main()
    flash('file Split Scuessfully')
    return redirect(url_for('index'))

def main():
    separator=Separator('spleeter:2stems')
    separator.separate_to_file('files/test.mp3','output/')

def makearchive(filename,dir_name):
    return shutil.make_archive(filename,'zip',dir_name)
def downloadfile(url):
    #url="https://firebasestorage.googleapis.com/v0/b/vocbot-264309.appspot.com/o/audio%2F9M90kSFtYTaa4Xj6TzDTcUEbVoB2%2F1.mp3?alt=media&token=2b734dd5-c279-4ae3-af6f-184a2d973e50"
    urllib.request.urlretrieve(url, "files/testnew.mp3")
if __name__=='__main__':
    app.run()
