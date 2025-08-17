#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$DIR"

# Activate virtual environment
source venv/bin/activate

# Launch the Flask app
python app.py