# Eco-Tourism Climate Risk Prediction

A machine learning-powered web application that predicts climate risks for eco-tourism destinations. The application uses both regression and classification models to provide comprehensive risk assessments for eco-tourism sites.

## Features

- Climate risk score prediction using regression model
- Flood risk category prediction using classification model
- Interactive web interface for data input
- RESTful API endpoints for predictions
- Real-time risk probability distribution
- Health check endpoint for monitoring

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: scikit-learn
- **Deployment**: Netlify
- **Data Processing**: pandas, numpy
- **Model Serialization**: joblib

## Prerequisites

- Python 3.9
- pip package manager
- Git

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd Eco-tourism-Climate-Risk-Prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
├── api/
│   ├── health.py
│   └── predict.py
├── static/
│   ├── script.js
│   └── styles.css
├── templates/
│   └── index.html
├── app.py
├── netlify.sh
├── netlify.toml
├── requirements.txt
├── runtime.txt
├── best_classification_model_logistic.pkl
├── best_regression_model_linear.pkl
├── classification_encoders.pkl
├── classification_scaler.pkl
├── regression_encoders.pkl
├── regression_scaler.pkl
└── feature_names.json
```

## Model Files

The application uses several pre-trained models and data processing files:
- `best_regression_model_linear.pkl`: Linear regression model for climate risk score prediction
- `best_classification_model_logistic.pkl`: Logistic regression model for flood risk classification
- `*_scaler.pkl`: Standard scalers for feature normalization
- `*_encoders.pkl`: Category encoders for categorical variables
- `feature_names.json`: List of feature names used by the models

## API Endpoints

### 1. Prediction Endpoint
- **URL**: `/api/predict`
- **Method**: POST
- **Required Fields**:
  - Latitude
  - Longitude
  - Vegetation_Type
  - Biodiversity_Index
  - Protected_Area_Status
  - Elevation_m
  - Slope_Degree
  - Soil_Type
  - Air_Quality_Index
  - Average_Temperature_C
  - Tourist_Attractions
  - Accessibility_Score
  - Tourist_Capacity_Limit

### 2. Health Check Endpoint
- **URL**: `/api/health`
- **Method**: GET
- **Response**: System health status and loaded models information

## Local Development

To run the application locally:

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Deployment on Netlify

1. Push your code to GitHub

2. Connect your repository to Netlify:
   - Go to Netlify dashboard
   - Click "New site from Git"
   - Select your repository
   - Configure build settings:
     - Build command: `bash netlify.sh`
     - Publish directory: `dist`

3. The application will be deployed and available at your Netlify URL

## Environment Variables

No environment variables are required for basic functionality. However, you can configure the following if needed:
- `PYTHON_VERSION`: Set in netlify.toml (default: 3.9)

## Input Data Format

Example of input JSON for prediction:
```json
{
  "Latitude": 35.6895,
  "Longitude": 139.6917,
  "Vegetation_Type": "Forest",
  "Biodiversity_Index": 0.75,
  "Protected_Area_Status": true,
  "Elevation_m": 40,
  "Slope_Degree": 15,
  "Soil_Type": "Clay",
  "Air_Quality_Index": 65,
  "Average_Temperature_C": 25,
  "Tourist_Attractions": 10,
  "Accessibility_Score": 0.8,
  "Tourist_Capacity_Limit": 1000
}
```

## Response Format

Example of prediction response:
```json
{
  "success": true,
  "climate_risk_score": 0.45,
  "flood_risk_category": "Medium",
  "risk_probabilities": {
    "Low": 0.2,
    "Medium": 0.6,
    "High": 0.2
  },
  "risk_level": "Medium"
}
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue in the GitHub repository.