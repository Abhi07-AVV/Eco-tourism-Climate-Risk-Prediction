#!/bin/bash
echo "Setting up Python environment..."
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Build completed successfully!"
