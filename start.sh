#!/bin/bash

# Billionaire Relationship Tracker - Startup Script

echo "=========================================="
echo "Billionaire Relationship Tracker"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Dependencies installed!"
echo ""

# Check if database exists
if [ ! -f "instance/billionaire_tracker.db" ]; then
    echo "Database not found. Creating and populating database..."
    python download_billionaires.py
    echo ""
fi

# Get billionaire count
BILLIONAIRE_COUNT=$(python -c "from app import create_app; from models import Billionaire; app = create_app(); app.app_context().push(); print(Billionaire.query.count())" 2>/dev/null)

if [ -z "$BILLIONAIRE_COUNT" ] || [ "$BILLIONAIRE_COUNT" -eq 0 ]; then
    echo "No billionaires found in database. Populating..."
    python download_billionaires.py
    echo ""
fi

echo "=========================================="
echo "Starting application..."
echo "=========================================="
echo ""
echo "The application will be available at:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python app.py
