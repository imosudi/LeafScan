
import time
from flask import  render_template, request, redirect, url_for, session
from datetime import datetime
import os, json
from werkzeug.utils import secure_filename

from .logic import tips_data, allowed_file, PlantDiagnosisEngine, diag_history
from . import app, ALLOWED_EXTENSIONS, diag_history_file

diag_history_path = diag_history_file #'diag_history.json'



@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        leaf_color      = request.form['leaf_color']
        spots           = request.form['spots']
        wilt            = request.form['wilt']
        leaf_curling    = request.form['leaf_curling']
        stunted_growth  = request.form['stunted_growth']
        leaf_drop       = request.form['leaf_drop']
        stem_damage     = request.form['stem_damage']
        unusual_smell   = request.form['unusual_smell']
        soil_condition  = request.form['soil_condition']
        notes           = request.form['notes']
        plant_type      = request.form['plant_type']
        plant_age       = request.form['plant_age']

        file = request.files.get('plant_image')
        image_url = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = url_for('static', filename='uploads/' + filename)

        # Advanced usage with additional symptoms
        additional_info = {
            'leaf_curling': leaf_curling,
            'stunted_growth': stunted_growth,
            'leaf_drop': leaf_drop,
            'stem_damage': stem_damage,
            'unusual_smell': unusual_smell,
            'soil_condition': soil_condition,
            'plant_type': plant_type,
            'plant_age': plant_age,
            'notes' : notes
        }
        # Initialise diagnosis engine
        diagnosis_system = PlantDiagnosisEngine()

        # Full diagnosis using all features
        diagnosis, explanation, treatment, severity, preventive_measures = diagnosis_system.diagnose_plant(
            leaf_color=leaf_color,
            spots=spots,
            wilt=wilt,
           additional_symptoms= additional_info 

            #leaf_curling=leaf_curling,
            #stunted_growth=stunted_growth,
            #leaf_drop=leaf_drop,
            #stem_damage=stem_damage,
            #unusual_smell=unusual_smell,
            #soil_condition=soil_condition,
            #plant_type=plant_type,
            #plant_age=plant_age,
            #notes=notes
        )

        # Save all inputs and results to history
        session['history'].append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'leaf_color': leaf_color,
            'spots': spots,
            'wilt': wilt,
            'leaf_curling': leaf_curling,
            'stunted_growth': stunted_growth,
            'leaf_drop': leaf_drop,
            'stem_damage': stem_damage,
            'unusual_smell': unusual_smell,
            'soil_condition': soil_condition,
            'plant_type': plant_type,
            'plant_age': plant_age,
            'notes': notes,
            'diagnosis': diagnosis,
            'explanation': explanation,
            'treatment': treatment,
            'severity': severity,
            'preventive_measures': preventive_measures,
            'image': image_url
        })

        session.modified = True
        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/tips')
def tips():
    return render_template('tips.html', tips=tips_data)


@app.route('/diagnosis', methods=['GET'])
def diagnosis():
    return render_template('diagnosis.html')

@app.route('/history')
def history():
    try:
        with open(diag_history_path, 'r') as f:
            diag_history = json.load(f)
            history_list = diag_history.get("history", [])
    except (FileNotFoundError, json.JSONDecodeError):
        history_list = []

    return render_template('history.html', history=history_list)



@app.route('/result', methods=['POST', 'GET'])
def result():
    try:
        with open(diag_history_path, 'r') as f:
            diag_history = json.load(f)
            history_list = diag_history.get("history", [])
    except (FileNotFoundError, json.JSONDecodeError):
        history_list = []

    if request.method == 'POST':
        leaf_color      = request.form['leaf_color']
        spots           = request.form['spots']
        wilt            = request.form['wilt']
        leaf_curling    = request.form['leaf_curling']
        stunted_growth  = request.form['stunted_growth']
        leaf_drop       = request.form['leaf_drop']
        stem_damage     = request.form['stem_damage']
        unusual_smell   = request.form['unusual_smell']
        soil_condition  = request.form['soil_condition']
        notes           = request.form['notes']
        plant_type      = request.form['plant_type']
        plant_age       = request.form['plant_age']

        file = request.files.get('plant_image')
        image_url = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = url_for('static', filename='uploads/' + filename)

        # Advanced usage with additional symptoms
        additional_info = {
            'leaf_curling': leaf_curling,
            'stunted_growth': stunted_growth,
            'leaf_drop': leaf_drop,
            'stem_damage': stem_damage,
            'unusual_smell': unusual_smell,
            'soil_condition': soil_condition,
            'plant_type': plant_type,
            'plant_age': plant_age,
            'notes' : notes
        }

        # Initialise diagnosis engine
        diagnosis_system = PlantDiagnosisEngine()

        # Full diagnosis using all features
        diagnosis, explanation, treatment, severity, preventive_measures = diagnosis_system.diagnose_plant(
            leaf_color=leaf_color,
            spots=spots,
            wilt=wilt,
           additional_symptoms= additional_info 
        )

        # Save all inputs and results to history
        latest = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'leaf_color': leaf_color,
            'spots': spots,
            'wilt': wilt,
            'leaf_curling': leaf_curling,
            'stunted_growth': stunted_growth,
            'leaf_drop': leaf_drop,
            'stem_damage': stem_damage,
            'unusual_smell': unusual_smell,
            'soil_condition': soil_condition,
            'plant_type': plant_type,
            'plant_age': plant_age,
            'notes': notes,
            'diagnosis': diagnosis,
            'explanation': explanation,
            'treatment': treatment,
            'severity': severity,
            'preventive_measures': preventive_measures,
            'image': image_url
        }
        # Append latest result to the diag_history object
        #diag_history["history"].append(latest)
        
        # Load existing history
        with open(diag_history_path, 'r') as f:
            diag_history = json.load(f)

        # Append new record
        diag_history["history"].append(latest)

        # Save back to JSON file
        with open(diag_history_path, 'w') as f:
            json.dump(diag_history, f, indent=4)

        return render_template('result.html', latest=latest,  history=history_list)#, diagnosis=diagnosis, explanation=explanation, treatment=treatment, severity=severity, preventive_measures=preventive_measures)

    return redirect('diagnosis')


