#!/usr/bin/env python3
"""
Verification script for advanced master's-level features.
This script checks if all the advanced features have been properly implemented.
"""

import os
import sys

def check_xai_features():
    """Check Explainable AI features."""
    print("Checking Explainable AI features...")
    
    # Check if SHAP is imported in message classifier
    message_classifier_path = os.path.join("backend", "models", "message_classifier.py")
    if os.path.exists(message_classifier_path):
        with open(message_classifier_path, 'r') as f:
            content = f.read()
            if "import shap" in content:
                print("  ✓ SHAP integration in message classifier")
            else:
                print("  ✗ SHAP not found in message classifier")
            
            if "explain_prediction" in content and "shap_explanation" in content:
                print("  ✓ SHAP explanation functionality")
            else:
                print("  ✗ SHAP explanation functionality missing")
    else:
        print("  ✗ Message classifier file not found")
    
    # Check if feature importance is in URL classifier
    url_classifier_path = os.path.join("backend", "models", "url_classifier.py")
    if os.path.exists(url_classifier_path):
        with open(url_classifier_path, 'r') as f:
            content = f.read()
            if "feature_importances_" in content:
                print("  ✓ Feature importance in URL classifier")
            else:
                print("  ✗ Feature importance not found in URL classifier")
    else:
        print("  ✗ URL classifier file not found")

def check_privacy_features():
    """Check privacy-preserving design features."""
    print("\nChecking Privacy-Preserving Design features...")
    
    # Check database schema for privacy features
    database_path = os.path.join("backend", "utils", "database.py")
    if os.path.exists(database_path):
        with open(database_path, 'r') as f:
            content = f.read()
            privacy_checks = [
                ("content_hash", "Content hashing"),
                ("content_preview", "Content preview"),
                ("privacy_settings", "Privacy settings table"),
                ("is_anonymized", "Anonymization flag")
            ]
            
            for check, description in privacy_checks:
                if check in content:
                    print(f"  ✓ {description}")
                else:
                    print(f"  ✗ {description} missing")
    else:
        print("  ✗ Database file not found")

def check_feedback_loop():
    """Check feedback loop implementation."""
    print("\nChecking Feedback Loop features...")
    
    # Check scan routes for feedback endpoint
    scan_routes_path = os.path.join("backend", "routes", "scan_routes.py")
    if os.path.exists(scan_routes_path):
        with open(scan_routes_path, 'r') as f:
            content = f.read()
            if "submit_feedback" in content and "FeedbackRequest" in content:
                print("  ✓ Feedback submission endpoint")
            else:
                print("  ✗ Feedback submission endpoint missing")
    else:
        print("  ✗ Scan routes file not found")
    
    # Check if feedback table exists in database
    database_path = os.path.join("backend", "utils", "database.py")
    if os.path.exists(database_path):
        with open(database_path, 'r') as f:
            content = f.read()
            if "CREATE TABLE IF NOT EXISTS feedback" in content:
                print("  ✓ Feedback table in database")
            else:
                print("  ✗ Feedback table missing from database")
    else:
        print("  ✗ Database file not found")

def check_cross_platform_consistency():
    """Check cross-platform consistency features."""
    print("\nChecking Cross-Platform Consistency features...")
    
    # Check risk service for platform insights
    risk_service_path = os.path.join("backend", "services", "risk_service.py")
    if os.path.exists(risk_service_path):
        with open(risk_service_path, 'r') as f:
            content = f.read()
            if "_get_platform_insights" in content:
                print("  ✓ Platform insights functionality")
            else:
                print("  ✗ Platform insights functionality missing")
            
            if "_generate_recommendations" in content:
                print("  ✓ Personalized recommendations")
            else:
                print("  ✗ Personalized recommendations missing")
    else:
        print("  ✗ Risk service file not found")

def check_advanced_api_schema():
    """Check advanced API schema features."""
    print("\nChecking Advanced API Schema features...")
    
    # Check scan schema for enhanced models
    scan_schema_path = os.path.join("backend", "schemas", "scan.py")
    if os.path.exists(scan_schema_path):
        with open(scan_schema_path, 'r') as f:
            content = f.read()
            schema_checks = [
                ("PrivacySettings", "Privacy settings model"),
                ("platform_insights", "Platform insights in risk score"),
                ("recommendations", "Recommendations in risk score"),
                ("scan_id", "Scan ID in scan result")
            ]
            
            for check, description in schema_checks:
                if check in content:
                    print(f"  ✓ {description}")
                else:
                    print(f"  ✗ {description} missing")
    else:
        print("  ✗ Scan schema file not found")

def check_user_interface_enhancements():
    """Check user interface enhancements."""
    print("\nChecking User Interface Enhancements...")
    
    # Check browser extension for feedback features
    popup_html_path = os.path.join("extension", "popup.html")
    if os.path.exists(popup_html_path):
        with open(popup_html_path, 'r') as f:
            content = f.read()
            if "feedbackSection" in content and "falsePositiveBtn" in content:
                print("  ✓ Feedback section in browser extension")
            else:
                print("  ✗ Feedback section missing from browser extension")
    else:
        print("  ✗ Browser extension popup HTML not found")
    
    # Check web dashboard for platform insights
    dashboard_path = os.path.join("web", "src", "components", "Dashboard.js")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r') as f:
            content = f.read()
            if "platformInsights" in content and "recommendations" in content:
                print("  ✓ Platform insights in web dashboard")
            else:
                print("  ✗ Platform insights missing from web dashboard")
    else:
        print("  ✗ Web dashboard file not found")

def main():
    """Main verification function."""
    print("Verifying Advanced Master's-Level Features")
    print("=" * 50)
    
    check_xai_features()
    check_privacy_features()
    check_feedback_loop()
    check_cross_platform_consistency()
    check_advanced_api_schema()
    check_user_interface_enhancements()
    
    print("\n" + "=" * 50)
    print("Verification complete!")
    print("\nFor a full verification, you would also want to:")
    print("1. Test the API endpoints with actual requests")
    print("2. Verify the database schema is properly created")
    print("3. Test the machine learning models with sample data")
    print("4. Verify the browser extension functionality in a browser")
    print("5. Test the web dashboard with a running backend")

if __name__ == "__main__":
    main()