from fastapi import APIRouter, HTTPException, status
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.scan import RiskScore
from services.risk_service import RiskService
from utils.database import get_db_connection

router = APIRouter(prefix="/risk", tags=["Risk Scoring"])

risk_service = RiskService()

@router.get("/score", response_model=RiskScore)
async def get_risk_score(token: str = None):
    """Get the current risk score for the authenticated user."""
    # In a real implementation, you would:
    # 1. Verify the token to get user ID
    # 2. Calculate risk score based on user's scan history
    # 3. Return the risk score
    
    # For now, we'll return a mock risk score
    mock_score = {
        "score": 45.5,
        "status": "yellow",
        "last_updated": "2023-01-01T00:00:00Z",
        "factors": {
            "breach_risk": {
                "score": 0.3,
                "weight": 0.3
            },
            "malicious_urls": {
                "score": 0.2,
                "weight": 0.25
            },
            "suspicious_messages": {
                "score": 0.6,
                "weight": 0.25
            },
            "password_risk": {
                "score": 0.1,
                "weight": 0.2
            }
        }
    }
    
    return RiskScore(**mock_score)

@router.get("/score/{user_id}", response_model=RiskScore)
async def get_user_risk_score(user_id: int):
    """Get the risk score for a specific user."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        )
    
    try:
        # Calculate risk score for the user
        risk_data = risk_service.calculate_risk_score(user_id, conn)
        conn.close()
        
        return RiskScore(**risk_data)
    
    except Exception as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate risk score: {str(e)}"
        )