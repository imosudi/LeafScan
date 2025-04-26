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

@app.route('/tips')
def tips():
    tips_data = [
        {
        'title': 'Avoid Overwatering',
        'content': 'Overwatering can cause root rot. Water your plants only when the topsoil feels dry to the touch.'
    },
    {
        'title': 'Use Well-Draining Soil',
        'content': 'Select soil that allows excess water to drain easily, preventing fungal infections in the roots.'
    },
    {
        'title': 'Provide Adequate Sunlight',
        'content': 'Ensure your plants receive the correct amount of sunlight each day, depending on their species.'
    },
    {
        'title': 'Inspect Leaves Regularly',
        'content': 'Check for early signs of diseases such as spots, mould, or discolouration, and treat promptly.'
    },
    {
        'title': 'Maintain Good Air Circulation',
        'content': 'Place plants in a way that allows air to flow between them, reducing the risk of fungal diseases.'
    },
    {
        'title': 'Use Organic Fertilisers',
        'content': 'Natural fertilisers enhance plant growth without the harmful chemicals that can weaken plant immunity.'
    },
    {
        'title': 'Prune Damaged Areas',
        'content': 'Remove dead or yellowing leaves promptly to prevent disease spread and encourage new growth.'
    },
    {
        'title': 'Rotate Plants Regularly',
        'content': 'Turn potted plants a quarter turn each week to ensure even growth and prevent leaning toward light sources.'
    },
    {
        'title': 'Monitor Humidity Levels',
        'content': 'Many plants thrive in higher humidity. Consider using a humidifier or pebble trays for tropical species.'
    },
    {
        'title': 'Repot When Necessary',
        'content': 'Repot plants when they become root-bound, typically every 1-2 years depending on growth rate.'
    },
    {
        'title': 'Clean Dust from Leaves',
        'content': 'Gently wipe leaves with a damp cloth to remove dust, which can block light absorption and respiration.'
    },
    {
        'title': 'Research Specific Needs',
        'content': 'Each plant species has unique requirements. Research your specific plants for optimal care.'
    },
    {
        'title': 'Use Appropriate Pot Sizes',
        'content': 'Choose pots that provide adequate room for root growth but aren\'t excessively large.'
    },
    {
        'title': 'Season-Specific Care',
        'content': 'Adjust watering, fertilizing, and light exposure based on seasonal growth patterns.'
    },
    {
        'title': 'Prevent Pest Infestations',
        'content': 'Regularly inspect for common pests like aphids and spider mites. Treat with natural solutions when possible.'
    },
    {
        'title': 'Quarantine New Plants',
        'content': 'Keep newly purchased plants isolated for 1-2 weeks to prevent potential pest spread to your existing collection.'
    },
    {
        'title': 'Avoid Temperature Extremes',
        'content': 'Keep plants away from cold drafts, heaters, and air conditioners that can cause stress and damage.'
    },
    {
        'title': 'Use Rainwater When Possible',
        'content': 'Rainwater is free of chemicals found in tap water that can build up in soil and harm sensitive plants.'
    },
    {
        'title': 'Group Plants by Needs',
        'content': 'Arrange plants with similar water, light, and humidity requirements together for more efficient care.'
    },
    {
        'title': 'Maintain Soil pH Balance',
        'content': 'Different plants thrive in different soil pH levels. Test and adjust soil pH for optimal nutrient absorption.'
    },
    {
        'title': 'Provide Support for Tall Plants',
        'content': 'Use stakes, trellises, or moss poles to support climbing plants and prevent stem damage.'
    },
    {
        'title': 'Practice Companion Planting',
        'content': 'Some plants benefit each other when grown together by repelling pests or enhancing growth patterns.'
    },
    {
        'title': 'Acclimate Plants Gradually',
        'content': 'When moving plants outdoors or to a brighter location, introduce them to new conditions gradually to prevent shock.'
    }
    ];
    return render_template('tips.html', tips=tips_data)


@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnos.html')

@app.route('/result')
def result():
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
        diagnosis, explanation, treatment, severity, preventive_measures = diagnosis_system.get_diagnosis_report(
            leaf_color=leaf_color,
            spots=spots,
            wilt=wilt,
           additional_symptoms= additional_info 
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

        return render_template('result.html', diagnosis=diagnosis, explanation=explanation, treatment=treatment, severity=severity, preventive_measures=preventive_measures)

    return render_template('result.html', latest=session['history'][-1], history=session['history'])
