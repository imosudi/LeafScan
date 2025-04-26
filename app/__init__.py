import time, os, platform, json
from flask import Flask
from flask_moment import Moment

from werkzeug.utils import secure_filename



app = Flask(__name__)
moment = Moment(app)


py_vers = (".").join(platform.python_version().split(".")[:2])
dir_path = os.path.dirname(os.path.realpath(__file__))#.strip("app")

app.secret_key  = 'this is a terrible secret it, if you break into this app you will be presecuted, if unconvicted, you will be persecuted and persecuted'
UPLOAD_FOLDER   = f'{dir_path}/static/uploads'
diag_history_file    = f'{dir_path}/diag_history.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    print("No Upload directory")
    os.makedirs(UPLOAD_FOLDER)

# Ensure the JSON file exists
if not os.path.exists(diag_history_file):
    with open(diag_history_file, 'w') as f:
        json.dump({"history": []}, f, indent=4)

from .routes import *