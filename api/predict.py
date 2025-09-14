"""
Vercel serverless function for ML predictions
"""
import os
import json
import joblib
import numpy as np
import pandas as pd
from http.server import BaseHTTPRequestHandler

# Global variables for models
models = {}
scalers = {}
encoders = {}
feature_names = {}

def load_models_and_processors():
    """Load all trained models and data processors"""
    global models, scalers, encoders, feature_names
    
    try:
        # Get the current directory (where the function is deployed)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        # Load models
        models['regression'] = joblib.load(os.path.join(parent_dir, 'best_regression_model_linear.pkl'))
        models['classification'] = joblib.load(os.path.join(parent_dir, 'best_classification_model_logistic.pkl'))
        
        # Load scalers
        scalers['regression'] = joblib.load(os.path.join(parent_dir, 'regression_scaler.pkl'))
        scalers['classification'] = joblib.load(os.path.join(parent_dir, 'classification_scaler.pkl'))
        
        # Load encoders
        encoders['regression'] = joblib.load(os.path.join(parent_dir, 'regression_encoders.pkl'))
        encoders['classification'] = joblib.load(os.path.join(parent_dir, 'classification_encoders.pkl'))
        
        # Load feature names
        with open(os.path.join(parent_dir, 'feature_names.json'), 'r') as f:
            feature_names = json.load(f)
            
        return True
        
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return False

def preprocess_input_data(data, task_type='regression'):
    """Preprocess input data same way as training data"""
    try:
        # Create DataFrame from input
        df = pd.DataFrame([data])
        
        # Handle categorical encoding
        categorical_features = ['Vegetation_Type', 'Soil_Type', 'Country']
        for feature in categorical_features:
            if feature in df.columns and feature in encoders[task_type]:
                encoder = encoders[task_type][feature]
                # Handle unknown categories by assigning 0
                df[feature] = df[feature].apply(
                    lambda x: encoder.transform([str(x)])[0] if str(x) in encoder.classes_ else 0
                )
        
        # Handle boolean column
        if 'Protected_Area_Status' in df.columns:
            df['Protected_Area_Status'] = df['Protected_Area_Status'].astype(int)
        
        # Select only feature columns needed for the model
        feature_cols = feature_names[f'{task_type}_features']
        df_features = df[feature_cols]
        
        # Scale features
        scaled_features = scalers[task_type].transform(df_features)
        
        return scaled_features
        
    except Exception as e:
        raise Exception(f"Error preprocessing data: {str(e)}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Load models if not already loaded
            if not models:
                success = load_models_and_processors()
                if not success:
                    self.send_error(500, 'Failed to load models')
                    return
            
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            input_data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            required_fields = [
                'Latitude', 'Longitude', 'Vegetation_Type', 'Biodiversity_Index',
                'Protected_Area_Status', 'Elevation_m', 'Slope_Degree', 'Soil_Type',
                'Air_Quality_Index', 'Average_Temperature_C', 'Tourist_Attractions',
                'Accessibility_Score', 'Tourist_Capacity_Limit'
            ]
            
            missing_fields = [field for field in required_fields if field not in input_data]
            if missing_fields:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': f'Missing required fields: {missing_fields}'}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Add default values for fields that might be missing but are needed by the model
            if 'Country' not in input_data:
                input_data['Country'] = 'USA'
            if 'Flood_Risk_Index' not in input_data:
                input_data['Flood_Risk_Index'] = 0.3
            if 'Drought_Risk_Index' not in input_data:
                input_data['Drought_Risk_Index'] = 0.3
            if 'Temperature_C' not in input_data:
                input_data['Temperature_C'] = input_data.get('Average_Temperature_C', 20.0)
            if 'Annual_Rainfall_mm' not in input_data:
                input_data['Annual_Rainfall_mm'] = 1000.0
            if 'Soil_Erosion_Risk' not in input_data:
                input_data['Soil_Erosion_Risk'] = 0.2
            if 'Current_Tourist_Count' not in input_data:
                input_data['Current_Tourist_Count'] = input_data.get('Tourist_Capacity_Limit', 500) * 0.6
            if 'Human_Activity_Index' not in input_data:
                input_data['Human_Activity_Index'] = 0.4
            if 'Conservation_Investment_USD' not in input_data:
                input_data['Conservation_Investment_USD'] = 100000.0
            if 'Climate_Risk_Score' not in input_data:
                input_data['Climate_Risk_Score'] = 0.4
            
            # Preprocess data for both models
            regression_data = preprocess_input_data(input_data, 'regression')
            classification_data = preprocess_input_data(input_data, 'classification')
            
            # Make predictions
            climate_risk_score = models['regression'].predict(regression_data)[0]
            flood_risk_prediction = models['classification'].predict(classification_data)[0]
            flood_risk_proba = models['classification'].predict_proba(classification_data)[0]
            
            # Convert predictions to user-friendly format
            risk_categories = ['Low', 'Medium', 'High']
            flood_risk_category = risk_categories[flood_risk_prediction] if flood_risk_prediction < len(risk_categories) else 'Unknown'
            
            # Create probability distribution
            risk_probabilities = {
                risk_categories[i]: float(flood_risk_proba[i]) if i < len(flood_risk_proba) else 0.0
                for i in range(len(risk_categories))
            }
            
            results = {
                'success': True,
                'climate_risk_score': float(climate_risk_score),
                'flood_risk_category': flood_risk_category,
                'risk_probabilities': risk_probabilities,
                'risk_level': 'Low' if climate_risk_score < 0.33 else 'Medium' if climate_risk_score < 0.67 else 'High'
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': str(e), 'success': False}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()