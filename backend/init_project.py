#!/usr/bin/env python3
"""
Project initialization script for the AI-Powered Personal Digital Safety Assistant.
This script sets up the database and creates initial model files.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from utils.database import init_db

def create_model_directories():
    """Create directories for model files."""
    model_dirs = [
        "models",
        "models/saved_models"
    ]
    
    for dir_path in model_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")

def create_sample_models():
    """Create sample model files for demonstration."""
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    
    # Create a simple message classifier model
    message_model_path = os.path.join(models_dir, "message_model.pkl")
    if not os.path.exists(message_model_path):
        with open(message_model_path, "w") as f:
            f.write("# Sample message classifier model\n")
            f.write("# In a real implementation, this would be a trained scikit-learn model\n")
        print(f"Created sample message model: {message_model_path}")
    
    # Create a simple URL classifier model
    url_model_path = os.path.join(models_dir, "url_model.pkl")
    if not os.path.exists(url_model_path):
        with open(url_model_path, "w") as f:
            f.write("# Sample URL classifier model\n")
            f.write("# In a real implementation, this would be a trained scikit-learn model\n")
        print(f"Created sample URL model: {url_model_path}")

def setup_database():
    """Set up the PostgreSQL database."""
    print("Initializing database...")
    success = init_db()
    if success:
        print("Database initialized successfully!")
    else:
        print("Failed to initialize database. Please check your PostgreSQL configuration.")

def main():
    """Main initialization function."""
    print("Initializing AI-Powered Personal Digital Safety Assistant...")
    
    # Create model directories
    create_model_directories()
    
    # Create sample models
    create_sample_models()
    
    # Set up database
    setup_database()
    
    print("\nInitialization complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure your PostgreSQL database settings in environment variables")
    print("3. Run the application: python main.py")

if __name__ == "__main__":
    main()