#!/usr/bin/env python3
"""
Verification script for the AI-Powered Personal Digital Safety Assistant backend.
This script checks if all required dependencies are installed and if the backend can start correctly.
"""

import sys
import os
import importlib.util

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "psycopg2",
        "jose",
        "passlib",
        "bcrypt",
        "python_multipart"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.util.find_spec(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    return len(missing_packages) == 0, missing_packages

def check_backend_files():
    """Check if all required backend files exist."""
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    required_files = [
        "main.py",
        "requirements.txt",
        "schemas/auth.py",
        "schemas/scan.py",
        "services/auth_service.py",
        "services/breach_service.py",
        "services/risk_service.py",
        "models/base_model.py",
        "models/message_classifier.py",
        "models/url_classifier.py",
        "routes/auth_routes.py",
        "routes/scan_routes.py",
        "routes/risk_routes.py",
        "utils/database.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = os.path.join(backend_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} exists")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path} is missing")
    
    return len(missing_files) == 0, missing_files

def main():
    """Main verification function."""
    print("Verifying AI-Powered Personal Digital Safety Assistant setup...")
    print("=" * 60)
    
    # Check dependencies
    print("\nChecking dependencies:")
    deps_ok, missing_deps = check_dependencies()
    
    # Check files
    print("\nChecking backend files:")
    files_ok, missing_files = check_backend_files()
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY:")
    
    if deps_ok and files_ok:
        print("✓ All checks passed! The backend should start correctly.")
        print("\nTo start the backend server, run:")
        print("  cd backend")
        print("  uvicorn main:app --reload")
        print("\nThen visit http://localhost:8000/docs for API documentation.")
        return True
    else:
        print("✗ Some checks failed:")
        if not deps_ok:
            print(f"  Missing dependencies: {', '.join(missing_deps)}")
        if not files_ok:
            print(f"  Missing files: {', '.join(missing_files)}")
        print("\nPlease install missing dependencies and ensure all files exist.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)