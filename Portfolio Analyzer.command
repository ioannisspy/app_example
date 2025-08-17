#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install flask pandas plotly
else
    # Activate virtual environment
    source venv/bin/activate
fi

echo "🚀 Starting Portfolio Analyzer..."
echo "📊 The web app will open in your browser automatically"
echo "🔗 If it doesn't open, go to: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Launch the Flask app
python app.py