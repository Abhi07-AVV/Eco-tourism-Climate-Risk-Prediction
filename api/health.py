"""
Vercel serverless function for health check
"""
import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Check if model files exist
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            
            model_files = [
                'best_regression_model_linear.pkl',
                'best_classification_model_logistic.pkl',
                'regression_scaler.pkl',
                'classification_scaler.pkl',
                'regression_encoders.pkl',
                'classification_encoders.pkl',
                'feature_names.json'
            ]
            
            missing_files = []
            for file in model_files:
                if not os.path.exists(os.path.join(parent_dir, file)):
                    missing_files.append(file)
            
            models_loaded = len(missing_files) == 0
            
            result = {
                'status': 'healthy' if models_loaded else 'partial',
                'models_loaded': models_loaded,
                'available_models': ['regression', 'classification'] if models_loaded else [],
                'missing_files': missing_files if missing_files else None
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()