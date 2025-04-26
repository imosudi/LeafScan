

from app import ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
Plant Disease Diagnosis System
This module provides comprehensive plant condition diagnosis based on multiple symptoms.
"""
class PlantDiagnosisEngine(object):
    def __init__(self, *args):
        self.version = "1.0"
        super(PlantDiagnosisEngine, self).__init__(*args)
        
    def diagnose_plant(self, leaf_color, spots, wilt, additional_symptoms=None):
        """
        Diagnose plant conditions based on symptoms.
        
        Parameters:
        -----------
        leaf_color : str
            Color of the leaves ('yellow', 'brown', 'green', 'pale_green', 'purple')
        spots : str
            Presence of spots on leaves ('yes', 'no', 'yellow_spots', 'black_spots', 'brown_spots')
        wilt : str
            Presence of wilting ('yes', 'no', 'severe', 'mild')
        additional_symptoms : dict, optional
            Additional symptoms that may help refine diagnosis:
            - 'leaf_curling': ('yes', 'no')
            - 'stunted_growth': ('yes', 'no')
            - 'leaf_drop': ('yes', 'no')
            - 'stem_damage': ('yes', 'no')
            - 'unusual_smell': ('yes', 'no')
            - 'soil_condition': ('dry', 'wet', 'normal')
            
        Returns:
        --------
        tuple
            (diagnosis, explanation, treatment, severity, preventive_measures)
        """
        # Initialize return values
        diagnosis = "Unknown condition"
        explanation = "Unable to determine a specific condition from the symptoms provided."
        treatment = "Consult a plant specialist for further evaluation."
        severity = "Unknown"
        preventive_measures = "Maintain regular care practices."
        
        # Default additional symptoms if none provided
        if additional_symptoms is None:
            additional_symptoms = {
                'leaf_curling': 'no',
                'stunted_growth': 'no',
                'leaf_drop': 'no',
                'stem_damage': 'no',
                'unusual_smell': 'no',
                'soil_condition': 'normal'
            }
        
        # Primary diagnostic rules based on core symptoms
        if leaf_color == 'yellow' and spots == 'yes' and wilt == 'yes':
            diagnosis = "Fungal Infection"
            explanation = "Yellowing, spots, and wilting often indicate fungal issues. The fungus may be attacking the vascular system, leading to overall plant decline."
            treatment = "Apply fungicide according to package instructions. Remove and destroy severely infected plant parts. Ensure adequate spacing between plants for air circulation."
            severity = "Moderate to Severe"
            preventive_measures = "Avoid overhead watering, maintain good air circulation, and sanitize garden tools."
            
            # Refined diagnosis based on additional symptoms
            if additional_symptoms.get('unusual_smell') == 'yes':
                diagnosis = "Advanced Fungal Infection"
                severity = "Severe"
            if additional_symptoms.get('soil_condition') == 'wet':
                explanation += " Wet soil conditions have likely contributed to this fungal growth."
                treatment += " Improve drainage and reduce watering frequency."
                
        elif leaf_color == 'yellow' and spots == 'no' and wilt == 'yes':
            diagnosis = "Root Rot"
            explanation = "Yellow leaves and wilting without spots suggest root damage, typically from overwatering or poor drainage leading to root rot."
            treatment = "Reduce watering immediately. Check for proper drainage. For potted plants, consider repotting in fresh soil with better drainage. For garden plants, improve soil drainage."
            severity = "Moderate"
            preventive_measures = "Water only when the top inch of soil is dry. Use well-draining soil and containers with drainage holes."
            
            if additional_symptoms.get('unusual_smell') == 'yes':
                diagnosis = "Severe Root Rot"
                explanation += " The unusual smell indicates advanced decay in the root system."
                severity = "Severe"
                
        elif leaf_color == 'brown' and spots == 'yes' and wilt == 'no':
            diagnosis = "Leaf Blight"
            explanation = "Brown color with spots is typical of leaf blight, a fungal disease that causes spotting and eventual tissue death on leaves."
            treatment = "Remove affected leaves. Apply appropriate fungicide. Ensure proper spacing between plants."
            severity = "Moderate"
            preventive_measures = "Avoid wetting foliage when watering. Remove plant debris promptly."
            
        elif leaf_color == 'brown' and spots == 'no' and wilt == 'yes':
            diagnosis = "Nutrient Deficiency"
            explanation = "Wilting and browning without spots may indicate lack of potassium or other essential nutrients."
            treatment = "Apply balanced fertilizer with emphasis on the deficient nutrient. Consider soil testing to identify specific deficiencies."
            severity = "Mild to Moderate"
            preventive_measures = "Maintain regular fertilization schedule appropriate for your plant species."
            
            if additional_symptoms.get('stunted_growth') == 'yes':
                diagnosis = "Severe Nutrient Deficiency"
                explanation += " The stunted growth confirms significant nutritional issues."
                severity = "Moderate to Severe"
                
        elif leaf_color == 'green' and spots == 'yes' and wilt == 'no':
            diagnosis = "Insect Damage"
            explanation = "Green leaves with spotting but no wilting suggest pest attacks. Insects may be feeding on the leaves or laying eggs, causing visible damage."
            treatment = "Identify the specific pest if possible. Apply appropriate insecticidal soap or neem oil. For severe infestations, consider stronger insecticides."
            severity = "Mild to Moderate"
            preventive_measures = "Regularly inspect plants for early signs of pests. Introduce beneficial insects when appropriate."
            
            if additional_symptoms.get('leaf_curling') == 'yes':
                diagnosis = "Aphid or Mite Infestation"
                explanation += " Leaf curling is particularly common with sap-sucking insects like aphids or mites."
                treatment = "Use insecticidal soap focusing on the undersides of leaves. Repeat treatment after 7-10 days."
                
        elif leaf_color == 'green' and spots == 'no' and wilt == 'yes':
            diagnosis = "Water Stress"
            if additional_symptoms.get('soil_condition') == 'dry':
                diagnosis = "Underwatering"
                explanation = "Wilting with green leaves in dry soil indicates water deficiency."
                treatment = "Water thoroughly until water drains from the bottom of the pot. For garden plants, water deeply to encourage deep root growth."
                severity = "Mild to Moderate"
                preventive_measures = "Establish a consistent watering schedule based on plant needs and environmental conditions."
            else:
                explanation = "Wilting with green leaves and no spots indicates water imbalance, either too much or too little water."
                treatment = "Check soil moisture level. Adjust watering accordingly."
                severity = "Mild"
                preventive_measures = "Monitor soil moisture regularly. Water only when needed."
                
        elif leaf_color == 'yellow' and spots == 'yes' and wilt == 'no':
            diagnosis = "Early Disease Stage"
            explanation = "Yellowing and spotting may indicate early-stage disease, possibly viral or bacterial infection."
            treatment = "Isolate the plant to prevent spread. Remove affected leaves. Monitor closely for development of additional symptoms."
            severity = "Mild to Moderate"
            preventive_measures = "Maintain plant vigor through proper care. Avoid overcrowding plants."
        
        # Additional comprehensive conditions
        elif leaf_color == 'pale_green' and spots == 'no' and wilt == 'no':
            diagnosis = "Nitrogen Deficiency"
            explanation = "Pale green leaves without other symptoms typically indicate nitrogen deficiency, essential for chlorophyll production."
            treatment = "Apply nitrogen-rich fertilizer according to package instructions. For organic options, consider blood meal or composted manure."
            severity = "Mild"
            preventive_measures = "Maintain regular fertilization schedule with balanced nutrients."
            
        elif leaf_color == 'purple' and spots == 'no' and wilt == 'no':
            diagnosis = "Phosphorus Deficiency"
            explanation = "Purple discoloration in leaves often indicates phosphorus deficiency, especially common in cold soil conditions."
            treatment = "Apply phosphorus-rich fertilizer. Ensure soil pH is appropriate for nutrient uptake."
            severity = "Mild"
            preventive_measures = "Test soil pH regularly and amend as needed. Use balanced fertilizer."
            
        elif leaf_color == 'yellow' and spots == 'no' and wilt == 'no':
            if additional_symptoms.get('leaf_curling') == 'yes':
                diagnosis = "Viral Infection"
                explanation = "Yellowing leaves with curling but no spots or wilting is consistent with certain viral infections."
                treatment = "Unfortunately, there is no cure for most plant viruses. Remove and destroy infected plants to prevent spread."
                severity = "Severe"
                preventive_measures = "Control insect vectors like aphids. Sanitize tools between plants."
            else:
                diagnosis = "Chlorosis"
                explanation = "General yellowing without other symptoms suggests chlorosis, often from iron deficiency or improper pH."
                treatment = "Apply iron supplement or adjust soil pH to improve nutrient availability."
                severity = "Mild"
                preventive_measures = "Test soil pH regularly and amend as needed."
                
        elif leaf_color == 'brown' and spots == 'no' and wilt == 'no':
            if additional_symptoms.get('leaf_drop') == 'yes':
                diagnosis = "Environmental Stress"
                explanation = "Browning leaves that drop without other symptoms often indicate environmental stress such as temperature extremes or transplant shock."
                treatment = "Stabilize environmental conditions. Provide shade if needed. Ensure consistent watering."
                severity = "Mild to Moderate"
                preventive_measures = "Gradually acclimate plants to new conditions. Protect from extreme weather."
            else:
                diagnosis = "Sunscald or Heat Stress"
                explanation = "Brown leaves without wilting or spots may indicate sunburn or heat stress."
                treatment = "Move plant to a location with appropriate light levels. For outdoor plants, provide temporary shade during hottest hours."
                severity = "Mild"
                preventive_measures = "Gradually acclimate plants to increased light levels."
                
        # Special case for black spots
        elif spots == 'black_spots':
            diagnosis = "Black Spot Fungus"
            explanation = "Black spots on leaves are characteristic of black spot fungus, a common rose disease that also affects other plants."
            treatment = "Remove and destroy affected leaves. Apply fungicide specifically formulated for black spot. Ensure good air circulation."
            severity = "Moderate"
            preventive_measures = "Avoid overhead watering. Clean up fallen leaves promptly."
        
        # Additional refinements based on other symptoms
        if additional_symptoms.get('stem_damage') == 'yes':
            explanation += " Stem damage present may indicate borer insects or mechanical injury."
            treatment += " Inspect stems carefully for entry holes if insect damage is suspected."
        
        if additional_symptoms.get('leaf_drop') == 'yes' and "leaf drop" not in explanation.lower():
            explanation += " Leaf drop indicates the plant is under significant stress."
            severity = self._increase_severity(severity)
        
        return diagnosis, explanation, treatment, severity, preventive_measures
    
    def _increase_severity(self, current_severity):
        """Increase the severity level by one step."""
        severity_levels = ["Unknown", "Mild", "Mild to Moderate", "Moderate", "Moderate to Severe", "Severe"]
        try:
            current_index = severity_levels.index(current_severity)
            if current_index < len(severity_levels) - 1:
                return severity_levels[current_index + 1]
            return current_severity
        except ValueError:
            return current_severity
    
    def get_diagnosis_report(self, leaf_color, spots, wilt, additional_symptoms=None):
        """
        Generate a formatted diagnosis report for the plant.
        
        Returns:
        --------
        str
            A formatted report with diagnosis details
        """
        diagnosis, explanation, treatment, severity, preventive_measures = self.diagnose_plant(
            leaf_color, spots, wilt, additional_symptoms
        )
        
        report = f"""
        PLANT DIAGNOSIS REPORT
        ======================
        
        DIAGNOSIS: {diagnosis}
        SEVERITY: {severity}
        
        EXPLANATION:
        {explanation}
        
        RECOMMENDED TREATMENT:
        {treatment}
        
        PREVENTIVE MEASURES:
        {preventive_measures}
        
        Note: This diagnosis is based on the symptoms provided. If the plant's condition 
        worsens or does not improve after following the recommendations, consult with 
        a professional horticulturist or plant pathologist.
        """
        
        return report.strip()

