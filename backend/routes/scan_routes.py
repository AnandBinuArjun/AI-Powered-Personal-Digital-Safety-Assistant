from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import json
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.scan import ScanRequest, ScanResult, ScanHistory, FeedbackRequest
from utils.database import get_db_connection, save_scan_result, get_user_privacy_settings
from services.auth_service import decode_access_token
from models.message_classifier import MessageClassifier
from models.url_classifier import URLClassifier
from services.breach_service import BreachService

router = APIRouter(prefix="/scan", tags=["Scanning"])

# Initialize models
message_model = MessageClassifier()
url_model = URLClassifier()
breach_service = BreachService()

def get_current_user(token: str):
    """Get current user from token."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return payload.get("sub")

@router.post("/analyze", response_model=ScanResult)
async def analyze_content(scan_request: ScanRequest, token: str = None):
    """Analyze content based on scan type."""
    user_id = None
    privacy_mode = False
    
    # Extract user information if token is provided
    if token:
        try:
            payload = decode_access_token(token)
            if payload:
                # In a real implementation, you would get user_id from database
                # For now, we'll use a placeholder
                user_id = 1  # Placeholder user ID
                # Get user privacy settings
                privacy_settings = get_user_privacy_settings(user_id)
                if privacy_settings:
                    privacy_mode = not privacy_settings.get("store_raw_content", False)
        except:
            # If token is invalid, continue without user info
            pass
    
    try:
        result = None
        
        if scan_request.scan_type == "message":
            # Analyze message for spam/scam
            prediction = message_model.predict(scan_request.content)
            explanation = message_model.explain_prediction(scan_request.content)
            
            result = {
                "prediction": prediction["prediction"],
                "confidence": prediction["confidence"],
                "details": explanation,
                "risk_score": _calculate_message_risk_score(prediction)
            }
            
        elif scan_request.scan_type == "url":
            # Analyze URL for malicious content
            prediction = url_model.predict(scan_request.content)
            explanation = url_model.explain_prediction(scan_request.content)
            
            result = {
                "prediction": prediction["prediction"],
                "confidence": prediction["confidence"],
                "details": explanation,
                "risk_score": _calculate_url_risk_score(prediction)
            }
            
        elif scan_request.scan_type == "email":
            # Check email for breaches
            breach_result = breach_service.check_email_breaches(scan_request.content)
            
            result = {
                "prediction": "breach_detected" if breach_result["breach_count"] > 0 else "safe",
                "confidence": min(breach_result["breach_count"] / 10.0, 1.0),
                "details": breach_result,
                "risk_score": _calculate_breach_risk_score(breach_result)
            }
            
        elif scan_request.scan_type == "password":
            # Check password safety
            password_result = breach_service.check_password_safety(scan_request.content)
            
            result = {
                "prediction": password_result["safety_status"],
                "confidence": 0.9 if password_result["safety_status"] == "compromised" else 0.1,
                "details": password_result,
                "risk_score": _calculate_password_risk_score(password_result)
            }
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported scan type: {scan_request.scan_type}"
            )
        
        # Save scan result to database (if user is authenticated)
        if user_id:
            try:
                scan_id = save_scan_result(user_id, scan_request.scan_type, scan_request.content, result, privacy_mode)
                # Add scan_id to result for feedback purposes
                result["scan_id"] = scan_id
            except Exception as e:
                print(f"Warning: Could not save scan result: {e}")
        
        return ScanResult(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

def _calculate_message_risk_score(prediction: dict) -> float:
    """Calculate risk score for message analysis."""
    if prediction["prediction"] == "scam":
        return prediction["confidence"] * 100
    elif prediction["prediction"] == "suspicious":
        return prediction["confidence"] * 50
    else:
        return prediction["confidence"] * 10

def _calculate_url_risk_score(prediction: dict) -> float:
    """Calculate risk score for URL analysis."""
    if prediction["prediction"] == "malicious":
        return prediction["confidence"] * 100
    elif prediction["prediction"] == "suspicious":
        return prediction["confidence"] * 50
    else:
        return prediction["confidence"] * 10

def _calculate_breach_risk_score(breach_result: dict) -> float:
    """Calculate risk score for breach detection."""
    # Normalize breach count to 0-100 scale
    return min(breach_result["breach_count"] * 10, 100)

def _calculate_password_risk_score(password_result: dict) -> float:
    """Calculate risk score for password safety."""
    if password_result["safety_status"] == "compromised":
        return 100
    else:
        return 0

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest, token: str = None):
    """Submit feedback for a scan result to improve the model."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        )
    
    try:
        cursor = conn.cursor()
        
        # Verify that the scan belongs to the user (if authenticated)
        user_id = None
        if token:
            try:
                payload = decode_access_token(token)
                if payload:
                    # In a real implementation, you would get user_id from database
                    user_id = 1  # Placeholder user ID
            except:
                pass
        
        # Insert feedback
        cursor.execute("""
            INSERT INTO feedback (user_id, scan_id, is_correct, comment)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (user_id, feedback.scan_id, feedback.is_correct, feedback.comment))
        
        feedback_id = cursor.fetchone()['id']
        conn.commit()
        cursor.close()
        conn.close()
        
        # In a real implementation, you would:
        # 1. Collect feedback data
        # 2. Periodically retrain models with feedback
        # 3. Update model performance metrics
        
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_id
        }
    
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )

@router.get("/history", response_model=List[ScanHistory])
async def get_scan_history(token: str = None):
    """Get scan history for the current user."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        )
    
    try:
        cursor = conn.cursor()
        
        # Get user ID from token
        user_id = None
        if token:
            try:
                payload = decode_access_token(token)
                if payload:
                    # In a real implementation, you would get user_id from database
                    user_id = 1  # Placeholder user ID
            except:
                pass
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Query database for user's scan history
        cursor.execute("""
            SELECT id, user_id, scan_type, content_preview, result, timestamp
            FROM scan_history 
            WHERE user_id = %s 
            ORDER BY timestamp DESC
            LIMIT 50
        """, (user_id,))
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Format results
        history = []
        for row in rows:
            history.append({
                "id": row['id'],
                "user_id": row['user_id'],
                "scan_type": row['scan_type'],
                "content": row['content_preview'] or "",
                "result": row['result'],
                "timestamp": row['timestamp']
            })
        
        return history
    
    except Exception as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve scan history: {str(e)}"
        )

@router.get("/privacy-settings")
async def get_privacy_settings(token: str = None):
    """Get user privacy settings."""
    # Get user ID from token
    user_id = None
    if token:
        try:
            payload = decode_access_token(token)
            if payload:
                # In a real implementation, you would get user_id from database
                user_id = 1  # Placeholder user ID
        except:
            pass
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    settings = get_user_privacy_settings(user_id)
    if not settings:
        # Return default settings
        settings = {
            "store_raw_content": False,
            "share_anonymous_data": True,
            "auto_delete_after_days": 365
        }
    
    return settings

@router.post("/privacy-settings")
async def update_privacy_settings(settings: dict, token: str = None):
    """Update user privacy settings."""
    # Get user ID from token
    user_id = None
    if token:
        try:
            payload = decode_access_token(token)
            if payload:
                # In a real implementation, you would get user_id from database
                user_id = 1  # Placeholder user ID
        except:
            pass
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    success = update_user_privacy_settings(user_id, settings)
    if success:
        return {"message": "Privacy settings updated successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update privacy settings"
        )