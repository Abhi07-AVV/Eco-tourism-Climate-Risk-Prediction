#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p dist
mkdir -p netlify/functions

# Copy static files and templates to dist directory
cp -r static dist/
cp -r templates/* dist/
cp -r *.pkl dist/
cp feature_names.json dist/

# Copy API files to Netlify functions
cp -r api/* netlify/functions/

# Create serverless functions for API endpoints
cat > netlify/functions/predict.js << EOL
const { createHandler } = require('@netlify/functions')
const app = require('../../app')

exports.handler = createHandler(app)
EOL

# Copy index.html to dist
cp templates/index.html dist/index.html

# Make scripts executable
chmod +x netlify/functions/*