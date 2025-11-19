from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ScanRequest(BaseModel):
    content: str
    scan_type: str  # "message", "url", "email", "password"

class ScanResult(BaseModel):
    prediction: str  # "safe", "suspicious", "scam"
    confidence: float
    details: Dict[str, Any]
    risk_score: float
    scan_id: Optional[int] = None

class ScanHistory(BaseModel):
    id: int
    user_id: int
    scan_type: str
    content: str
    result: ScanResult
    timestamp: datetime

class FeedbackRequest(BaseModel):
    scan_id: int
    is_correct: bool
    comment: Optional[str] = None

class PrivacySettings(BaseModel):
    store_raw_content: bool = False
    share_anonymous_data: bool = True
    auto_delete_after_days: int = 365

class RiskScore(BaseModel):
    score: float
    status: str  # "green", "yellow", "red"
    last_updated: datetime
    factors: Dict[str, Any]
    platform_insights: Dict[str, Any]
    recommendations: List[str]

class MessageAnalysisDetails(BaseModel):
    text_explanation: List[str]
    feature_importance: Dict[str, Any]
    shap_explanation: Optional[Dict[str, Any]] = None

class URLAnalysisDetails(BaseModel):
    features: Dict[str, float]
    concerns: List[Dict[str, Any]]
    text_explanation: List[str]
    feature_importance: Dict[str, Any]