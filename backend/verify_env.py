#!/usr/bin/env python3
"""
Script to verify that environment variables are loaded correctly.
"""

import os
from dotenv import load_dotenv

def verify_env_variables():
    """Verify that environment variables are loaded correctly."""
    # Load environment variables from .env file
    load_dotenv()
    
    print("Environment Variables Verification")
    print("=" * 40)
    
    # Check database variables
    db_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]
    
    print("Database Configuration:")
    for var in db_vars:
        value = os.getenv(var, "NOT SET")
        # Mask sensitive values
        if "PASSWORD" in var and value != "NOT SET":
            value = "*" * len(value)
        print(f"  {var}: {value}")
    
    print("\nSecurity Settings:")
    security_vars = [
        "SECRET_KEY",
        "JWT_SECRET_KEY"
    ]
    
    for var in security_vars:
        value = os.getenv(var, "NOT SET")
        # Mask sensitive values
        if value != "NOT SET":
            value = "*" * min(len(value), 20) + ("..." if len(value) > 20 else "")
        print(f"  {var}: {value}")
    
    print("\nFrontend URLs:")
    frontend_vars = [
        "FRONTEND_URL_LOCAL",
        "FRONTEND_URL_ANDROID",
        "FRONTEND_URL_EXTENSION"
    ]
    
    for var in frontend_vars:
        value = os.getenv(var, "NOT SET")
        print(f"  {var}: {value}")
    
    print("\nTesting Configuration:")
    test_vars = [
        "DEBUG",
        "TESTING"
    ]
    
    for var in test_vars:
        value = os.getenv(var, "NOT SET")
        print(f"  {var}: {value}")
    
    print("\nModel Paths:")
    model_vars = [
        "MESSAGE_MODEL_PATH",
        "URL_MODEL_PATH"
    ]
    
    for var in model_vars:
        value = os.getenv(var, "NOT SET")
        print(f"  {var}: {value}")
    
    print("\n" + "=" * 40)
    print("Verification complete!")

if __name__ == "__main__":
    verify_env_variables()