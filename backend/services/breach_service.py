import hashlib
import requests
from typing import Dict, Any, List

class BreachService:
    """Service for checking email breaches and password safety."""
    
    def __init__(self):
        # In a real implementation, this would connect to a breach database
        # For simulation, we'll use a mock database
        self.mock_breaches = {
            "compromised@example.com": [
                {"name": "LinkedIn Breach 2021", "date": "2021-06-15", "count": 7500000},
                {"name": "Adobe Breach 2013", "date": "2013-10-04", "count": 152445165}
            ],
            "test@example.com": [
                {"name": "Mock Data Breach", "date": "2022-01-01", "count": 10000}
            ]
        }
    
    def check_email_breaches(self, email: str) -> Dict[str, Any]:
        """Check if an email has been involved in data breaches."""
        # In a real implementation, this would call the HIBP API or similar
        # For now, we'll use mock data
        breaches = self.mock_breaches.get(email.lower(), [])
        
        return {
            "email": email,
            "breach_count": len(breaches),
            "breaches": breaches,
            "risk_level": self._calculate_breach_risk(len(breaches))
        }
    
    def check_password_safety(self, password: str) -> Dict[str, Any]:
        """Check password safety using k-anonymity method."""
        # Calculate SHA-1 hash of the password
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        # In a real implementation, this would call the HIBP API
        # For simulation, we'll use mock data
        mock_pwned_hashes = {
            "CBFDAC": 5,  # Password "password" appears 5 times
            "71E2F0": 3,  # Another common password
        }
        
        count = mock_pwned_hashes.get(prefix[:6], 0)
        
        return {
            "password_hash_prefix": prefix,
            "compromised_count": count,
            "safety_status": "compromised" if count > 0 else "safe",
            "recommendation": self._get_password_recommendation(count)
        }
    
    def _calculate_breach_risk(self, breach_count: int) -> str:
        """Calculate breach risk level based on number of breaches."""
        if breach_count == 0:
            return "low"
        elif breach_count <= 2:
            return "medium"
        else:
            return "high"
    
    def _get_password_recommendation(self, compromise_count: int) -> str:
        """Get password recommendation based on compromise count."""
        if compromise_count == 0:
            return "Your password was not found in known data breaches. Good job!"
        elif compromise_count <= 10:
            return "Your password has appeared in a few data breaches. Consider changing it."
        else:
            return "Your password has appeared in many data breaches! Change it immediately and never reuse it."

# In a real implementation, you would integrate with the HIBP API:
# def check_email_breaches_real(self, email: str) -> Dict[str, Any]:
#     """Real implementation using HIBP API."""
#     headers = {
#         'hibp-api-key': 'YOUR_API_KEY',
#         'user-agent': 'SafetyAssistant'
#     }
#     
#     try:
#         response = requests.get(
#             f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
#             headers=headers
#         )
#         response.raise_for_status()
#         
#         breaches = response.json()
#         return {
#             "email": email,
#             "breach_count": len(breaches),
#             "breaches": breaches,
#             "risk_level": self._calculate_breach_risk(len(breaches))
#         }
#     except requests.exceptions.RequestException as e:
#         return {
#             "error": f"Failed to check breaches: {str(e)}"
#         }