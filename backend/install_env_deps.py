#!/usr/bin/env python3
"""
Script to install environment-related dependencies for the backend.
"""

import subprocess
import sys

def install_dotenv():
    """Install python-dotenv package."""
    try:
        print("Installing python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        print("✓ python-dotenv installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install python-dotenv: {e}")

def install_tldextract():
    """Install tldextract package."""
    try:
        print("Installing tldextract...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tldextract"])
        print("✓ tldextract installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install tldextract: {e}")

def main():
    """Main installation function."""
    print("Installing environment-related dependencies...")
    
    install_dotenv()
    install_tldextract()
    
    print("\nEnvironment-related dependencies installation completed!")
    print("\nTo use the .env file, make sure to:")
    print("1. Update the values in backend/.env with your actual credentials")
    print("2. Restart the backend server to load the new environment variables")

if __name__ == "__main__":
    main()