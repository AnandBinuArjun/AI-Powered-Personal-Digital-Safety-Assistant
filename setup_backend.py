#!/usr/bin/env python3
"""
Simple setup script for the AI-Powered Personal Digital Safety Assistant backend.
This script installs only the essential dependencies to get the backend running.
"""

import subprocess
import sys
import os

def install_essential_backend_dependencies():
    """Install essential backend dependencies."""
    print("Installing essential backend dependencies...")
    
    # Essential packages needed for the backend
    essential_packages = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "psycopg2-binary",
        "python-jose",
        "passlib",
        "bcrypt",
        "python-multipart"
    ]
    
    try:
        # Install each package
        for package in essential_packages:
            print(f"Installing {package}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"Successfully installed {package}")
            else:
                print(f"Error installing {package}:")
                print(result.stderr)
                
    except Exception as e:
        print(f"Error during dependency installation: {e}")

def main():
    """Main setup function."""
    print("Setting up AI-Powered Personal Digital Safety Assistant backend...")
    
    # Install essential backend dependencies
    install_essential_backend_dependencies()
    
    print("\nEssential backend dependencies installation completed!")
    print("\nNext steps:")
    print("1. Install PostgreSQL database if not already installed")
    print("2. Configure your PostgreSQL database settings in environment variables")
    print("3. Run the backend initialization: python backend/init_project.py")
    print("4. Start the backend server: uvicorn backend.main:app --reload")

if __name__ == "__main__":
    main()