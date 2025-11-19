#!/usr/bin/env python3
"""
Script to install dependencies for the AI-Powered Personal Digital Safety Assistant.
"""

import subprocess
import sys
import os

def install_backend_dependencies():
    """Install backend dependencies."""
    print("Installing backend dependencies...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    original_dir = os.getcwd()
    
    try:
        os.chdir(backend_dir)
        
        # Install requirements
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Backend dependencies installed successfully!")
            print(result.stdout)
        else:
            print("Error installing backend dependencies:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error during backend dependency installation: {e}")
    finally:
        os.chdir(original_dir)

def install_web_dependencies():
    """Install web dependencies."""
    print("Installing web dependencies...")
    
    # Change to web directory
    web_dir = os.path.join(os.path.dirname(__file__), "web")
    original_dir = os.getcwd()
    
    try:
        os.chdir(web_dir)
        
        # Install npm packages
        result = subprocess.run(
            ["npm", "install"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Web dependencies installed successfully!")
            print(result.stdout)
        else:
            print("Error installing web dependencies:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error during web dependency installation: {e}")
    finally:
        os.chdir(original_dir)

def install_android_dependencies():
    """Install Android/Flutter dependencies."""
    print("Installing Android/Flutter dependencies...")
    
    # Change to android directory
    android_dir = os.path.join(os.path.dirname(__file__), "android")
    original_dir = os.getcwd()
    
    try:
        os.chdir(android_dir)
        
        # Run flutter pub get
        result = subprocess.run(
            ["flutter", "pub", "get"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Android/Flutter dependencies installed successfully!")
            print(result.stdout)
        else:
            print("Error installing Android/Flutter dependencies:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error during Android/Flutter dependency installation: {e}")
    finally:
        os.chdir(original_dir)

def main():
    """Main installation function."""
    print("Installing dependencies for AI-Powered Personal Digital Safety Assistant...")
    
    # Install backend dependencies
    install_backend_dependencies()
    
    # Install web dependencies
    install_web_dependencies()
    
    # Install Android dependencies
    install_android_dependencies()
    
    print("\nDependency installation process completed!")
    print("\nNext steps:")
    print("1. Configure your PostgreSQL database settings in environment variables")
    print("2. Run the backend initialization: python backend/init_project.py")
    print("3. Start the backend server: uvicorn backend.main:app --reload")
    print("4. Start the web dashboard: cd web && npm start")
    print("5. For Android app: cd android && flutter run")

if __name__ == "__main__":
    main()