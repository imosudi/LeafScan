import time
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from .logic import allowed_file,PlantDiagnosisEngine
from . import app, ALLOWED_EXTENSIONS




# Rules and diagnosis engine
def diagnose_plant(leaf_color, spots, wilt):
    explanation = ""
    diagnosis = "Unknown condition"

    if leaf_color == 'yellow' and spots == 'yes' and wilt == 'yes':
        diagnosis = "Fungal Infection"
        explanation = "Yellowing, spots, and wilting often indicate fungal issues."
    elif leaf_color == 'yellow' and spots == 'no' and wilt == 'yes':
        diagnosis = "Root Rot"
        explanation = "Yellow leaves and wilting without spots suggest root damage."
    elif leaf_color == 'brown' and spots == 'yes' and wilt == 'no':
        diagnosis = "Leaf Blight"
        explanation = "Brown colour with spots is typical of leaf blight."
    elif leaf_color == 'brown' and spots == 'no' and wilt == 'yes':
        diagnosis = "Nutrient Deficiency"
        explanation = "Wilting and browning without spots may indicate lack of potassium."
    elif leaf_color == 'green' and spots == 'yes' and wilt == 'no':
        diagnosis = "Insect Damage"
        explanation = "Green leaves with spotting but no wilting suggest pest attacks."
    elif leaf_color == 'green' and spots == 'no' and wilt == 'yes':
        diagnosis = "Water Stress"
        explanation = "Wilting with green leaves and no spots indicates water imbalance."
    elif leaf_color == 'yellow' and spots == 'yes' and wilt == 'no':
        diagnosis = "Early Disease Stage"
        explanation = "Yellowing and spotting may indicate early-stage disease."

    return diagnosis, explanation

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

        # Full diagnosis using all features (make sure your class handles this)
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

@app.route('/result')
def result():
    return render_template('result.html', latest=session['history'][-1], history=session['history'])
