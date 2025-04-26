import time
from flask import Flask, render_template, request, redirect, url_for, session
from flask_moment import Moment
from datetime import datetime
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
moment = Moment(app)


app.secret_key = 'this is a terrible secret it, if you break into this app you will be presecuted, if unconvicted, you will be persecuted and persecuted'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


from .routes import *