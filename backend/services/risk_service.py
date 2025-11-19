from typing import Dict, Any, List
from datetime import datetime, timedelta
import numpy as np

class RiskService:
    """Service for calculating personal cyber safety scores with cross-platform consistency."""
    
    def __init__(self):
        # Weight factors for different risk components
        self.weights = {
            "breach_risk": 0.3,
            "malicious_urls": 0.25,
            "suspicious_messages": 0.25,
            "password_risk": 0.2
        }
    
    def calculate_risk_score(self, user_id: int, db) -> Dict[str, Any]:
        """Calculate the overall risk score for a user with cross-platform consistency."""
        # Get user scan history from all platforms
        scan_history = self._get_user_scan_history(user_id, db)
        
        # Calculate individual risk factors
        breach_risk = self._calculate_breach_risk(user_id, db)
        url_risk = self._calculate_url_risk(scan_history)
        message_risk = self._calculate_message_risk(scan_history)
        password_risk = self._calculate_password_risk(scan_history)
        
        # Calculate weighted score (0-100 scale)
        risk_score = (
            breach_risk * self.weights["breach_risk"] +
            url_risk * self.weights["malicious_urls"] +
            message_risk * self.weights["suspicious_messages"] +
            password_risk * self.weights["password_risk"]
        ) * 100
        
        # Determine status based on score
        status = self._determine_status(risk_score)
        
        # Get platform-specific insights
        platform_insights = self._get_platform_insights(scan_history)
        
        return {
            "score": round(risk_score, 2),
            "status": status,
            "last_updated": datetime.now().isoformat(),
            "factors": {
                "breach_risk": {
                    "score": breach_risk,
                    "weight": self.weights["breach_risk"]
                },
                "malicious_urls": {
                    "score": url_risk,
                    "weight": self.weights["malicious_urls"]
                },
                "suspicious_messages": {
                    "score": message_risk,
                    "weight": self.weights["suspicious_messages"]
                },
                "password_risk": {
                    "score": password_risk,
                    "weight": self.weights["password_risk"]
                }
            },
            "platform_insights": platform_insights,
            "recommendations": self._generate_recommendations(
                breach_risk, url_risk, message_risk, password_risk
            )
        }
    
    def _get_user_scan_history(self, user_id: int, db) -> List[Dict]:
        """Get user's scan history from all platforms."""
        cursor = db.cursor()
        cursor.execute("""
            SELECT scan_type, result, timestamp 
            FROM scan_history 
            WHERE user_id = %s 
            ORDER BY timestamp DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        cursor.close()
        
        return [dict(row) for row in rows]
    
    def _calculate_breach_risk(self, user_id: int, db) -> float:
        """Calculate breach risk factor."""
        cursor = db.cursor()
        cursor.execute("""
            SELECT COUNT(*) as breach_count
            FROM scan_history 
            WHERE user_id = %s AND scan_type = 'email'
        """, (user_id,))
        
        result = cursor.fetchone()
        cursor.close()
        
        breach_count = result['breach_count'] if result else 0
        
        # Normalize to 0-1 scale (assuming max 10 breaches is high risk)
        return min(breach_count / 10.0, 1.0)
    
    def _calculate_url_risk(self, scan_history: List[Dict]) -> float:
        """Calculate URL risk factor based on malicious URL detections."""
        url_scans = [scan for scan in scan_history if scan['scan_type'] == 'url']
        
        if not url_scans:
            return 0.0
        
        malicious_count = 0
        for scan in url_scans:
            result = scan.get('result', {})
            if isinstance(result, dict) and result.get('prediction') in ['malicious', 'scam']:
                malicious_count += 1
        
        # Normalize to 0-1 scale (assuming max 5 malicious URLs is high risk)
        return min(malicious_count / 5.0, 1.0)
    
    def _calculate_message_risk(self, scan_history: List[Dict]) -> float:
        """Calculate message risk factor based on suspicious message detections."""
        message_scans = [scan for scan in scan_history if scan['scan_type'] == 'message']
        
        if not message_scans:
            return 0.0
        
        suspicious_count = 0
        for scan in message_scans:
            result = scan.get('result', {})
            if isinstance(result, dict) and result.get('prediction') in ['suspicious', 'scam']:
                suspicious_count += 1
        
        # Normalize to 0-1 scale (assuming max 10 suspicious messages is high risk)
        return min(suspicious_count / 10.0, 1.0)
    
    def _calculate_password_risk(self, scan_history: List[Dict]) -> float:
        """Calculate password risk factor based on compromised password detections."""
        password_scans = [scan for scan in scan_history if scan['scan_type'] == 'password']
        
        if not password_scans:
            return 0.0
        
        compromised_count = 0
        for scan in password_scans:
            result = scan.get('result', {})
            if isinstance(result, dict) and result.get('safety_status') == 'compromised':
                compromised_count += 1
        
        # Normalize to 0-1 scale (assuming max 3 compromised passwords is high risk)
        return min(compromised_count / 3.0, 1.0)
    
    def _determine_status(self, risk_score: float) -> str:
        """Determine risk status based on score."""
        if risk_score < 30:
            return "green"
        elif risk_score < 70:
            return "yellow"
        else:
            return "red"
    
    def _get_platform_insights(self, scan_history: List[Dict]) -> Dict[str, Any]:
        """Get insights by platform for cross-platform consistency."""
        platforms = {
            "android": {"scans": 0, "risks": 0},
            "web": {"scans": 0, "risks": 0},
            "browser_extension": {"scans": 0, "risks": 0}
        }
        
        # In a real implementation, you would track platform information
        # For now, we'll distribute scans evenly as an example
        total_scans = len(scan_history)
        if total_scans > 0:
            scans_per_platform = total_scans // 3
            remainder = total_scans % 3
            
            platforms["android"]["scans"] = scans_per_platform + (1 if remainder > 0 else 0)
            platforms["web"]["scans"] = scans_per_platform + (1 if remainder > 1 else 0)
            platforms["browser_extension"]["scans"] = scans_per_platform
            
            # Calculate risk distribution (simplified)
            risk_per_platform = 1.0 / 3  # Even distribution for demo
            platforms["android"]["risks"] = risk_per_platform
            platforms["web"]["risks"] = risk_per_platform
            platforms["browser_extension"]["risks"] = risk_per_platform
        
        return platforms
    
    def _generate_recommendations(self, breach_risk: float, url_risk: float, 
                                message_risk: float, password_risk: float) -> List[str]:
        """Generate personalized recommendations based on risk factors."""
        recommendations = []
        
        if breach_risk > 0.5:
            recommendations.append("Review your accounts for data breaches and change passwords")
        
        if url_risk > 0.5:
            recommendations.append("Be cautious when clicking links, especially in emails or messages")
        
        if message_risk > 0.5:
            recommendations.append("Enable scam detection on all messaging platforms")
        
        if password_risk > 0.5:
            recommendations.append("Use a password manager and enable two-factor authentication")
        
        if not recommendations:
            recommendations.append("Continue practicing good cybersecurity habits")
            recommendations.append("Regularly update your security knowledge")
        
        return recommendations