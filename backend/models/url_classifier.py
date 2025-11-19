import pickle
import numpy as np
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import tldextract
from typing import Dict, Any, List
from .base_model import BaseModel

class URLClassifier(BaseModel):
    """URL classification model for detecting malicious websites."""
    
    def __init__(self, model_path: str = "models/url_model.pkl"):
        self.model_path = model_path
        self.scaler = StandardScaler()
        self.label_map = {0: "safe", 1: "suspicious", 2: "malicious"}
        # Initialize a default model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def load_model(self):
        """Load the trained model from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                if isinstance(data, dict) and 'model' in data and 'scaler' in data:
                    self.model = data['model']
                    self.scaler = data['scaler']
                else:
                    self.model = data
        except (FileNotFoundError, pickle.UnpicklingError):
            # Initialize a default model if file doesn't exist or is invalid
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def extract_features(self, url: str) -> List[float]:
        """Extract features from a URL for classification."""
        features = []
        
        # Parse URL
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query
        
        # Extract domain parts
        extracted = tldextract.extract(url)
        subdomain = extracted.subdomain
        domain_name = extracted.domain
        suffix = extracted.suffix
        
        # Feature 1: URL length
        features.append(len(url))
        
        # Feature 2: Domain length
        features.append(len(domain))
        
        # Feature 3: Path length
        features.append(len(path))
        
        # Feature 4: Number of dots in URL
        features.append(url.count('.'))
        
        # Feature 5: Number of slashes in URL
        features.append(url.count('/'))
        
        # Feature 6: Number of dashes in URL
        features.append(url.count('-'))
        
        # Feature 7: Number of underscores in URL
        features.append(url.count('_'))
        
        # Feature 8: Number of question marks in URL
        features.append(url.count('?'))
        
        # Feature 9: Number of equal signs in URL
        features.append(url.count('='))
        
        # Feature 10: Number of ampersands in URL
        features.append(url.count('&'))
        
        # Feature 11: Number of percent signs in URL
        features.append(url.count('%'))
        
        # Feature 12: Number of subdomains
        features.append(subdomain.count('.') + 1 if subdomain else 0)
        
        # Feature 13: Presence of IP address
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        features.append(1 if re.search(ip_pattern, domain) else 0)
        
        # Feature 14: Presence of suspicious keywords
        suspicious_keywords = ['secure', 'account', 'update', 'confirm', 'login', 'signin', 'bank', 'paypal', 'amazon']
        suspicious_count = sum(1 for keyword in suspicious_keywords if keyword in url.lower())
        features.append(suspicious_count)
        
        # Feature 15: URL entropy (randomness)
        def calculate_entropy(s):
            import math
            if not s:
                return 0
            entropy = 0
            for char in set(s):
                p = s.count(char) / len(s)
                entropy -= p * math.log2(p)
            return entropy
        
        features.append(calculate_entropy(url))
        
        # Feature 16: Number of parameters
        features.append(query.count('&') + 1 if query else 0)
        
        # Feature 17: Presence of @ symbol (often used in phishing)
        features.append(1 if '@' in url else 0)
        
        # Feature 18: Presence of port number (unusual ports)
        features.append(1 if ':' in domain and not any(port in domain for port in [':80', ':443']) else 0)
        
        return features
    
    def get_feature_names(self) -> List[str]:
        """Get names of extracted features."""
        return [
            "URL Length", "Domain Length", "Path Length", "Dots Count", "Slashes Count",
            "Dashes Count", "Underscores Count", "Question Marks Count", "Equal Signs Count",
            "Ampersands Count", "Percent Signs Count", "Subdomain Count", "IP Address Present",
            "Suspicious Keywords Count", "URL Entropy", "Parameter Count", "@ Symbol Present",
            "Unusual Port Present"
        ]
    
    def preprocess(self, url: str) -> np.ndarray:
        """Preprocess the URL for model input."""
        features = self.extract_features(url)
        # Reshape for single sample
        return np.array(features).reshape(1, -1)
    
    def train(self, urls: list, labels: list):
        """Train the model with provided data."""
        # Extract features for all URLs
        X = np.array([self.extract_features(url) for url in urls])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, labels)
        
        # Save the trained model and scaler
        with open(self.model_path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def predict(self, url: str) -> Dict[str, Any]:
        """Predict if a URL is safe, suspicious, or malicious."""
        # Extract and scale features
        features = self.preprocess(url)
        if hasattr(self, 'scaler'):
            features = self.scaler.transform(features)
        
        # Get prediction
        prediction = self.model.predict(features)[0]
        
        # Get prediction probabilities
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(features)[0]
            confidence = float(np.max(probabilities))
        else:
            probabilities = [0.0] * len(self.label_map)
            confidence = 1.0
        
        return {
            "prediction": self.label_map.get(prediction, "unknown"),
            "confidence": confidence,
            "probabilities": {
                self.label_map[i]: float(prob) for i, prob in enumerate(probabilities)
            }
        }
    
    def explain_prediction(self, url: str) -> Dict[str, Any]:
        """Provide detailed explanation for the URL prediction with feature importance."""
        features = self.extract_features(url)
        feature_names = self.get_feature_names()
        
        # Get feature importance if available
        feature_importance = {}
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            # Sort features by importance
            feature_importance_list = [(feature_names[i], importances[i], features[i]) 
                                     for i in range(len(feature_names))]
            feature_importance_list.sort(key=lambda x: x[1], reverse=True)
            
            feature_importance = {
                "top_features": [
                    {
                        "feature": name,
                        "importance": float(importance),
                        "value": float(value)
                    }
                    for name, importance, value in feature_importance_list[:10]
                ]
            }
        
        # Identify concerning features with detailed explanations
        concerns = []
        
        # Check for unusually long URL
        if features[0] > 100:  # URL length
            concerns.append({
                "feature": "URL Length",
                "value": features[0],
                "reason": "Unusually long URL may indicate obfuscation",
                "severity": "high" if features[0] > 150 else "medium"
            })
        
        # Check for IP address
        if features[12] > 0:  # IP address present
            concerns.append({
                "feature": "IP Address",
                "value": "Present",
                "reason": "Direct IP addresses in URLs are often used by malicious sites",
                "severity": "high"
            })
        
        # Check for high entropy
        if features[14] > 4:  # High entropy
            concerns.append({
                "feature": "URL Entropy",
                "value": round(features[14], 2),
                "reason": "High randomness in URL may indicate obfuscation",
                "severity": "high" if features[14] > 5 else "medium"
            })
        
        # Check for many suspicious keywords
        if features[13] > 2:  # Suspicious keywords count
            concerns.append({
                "feature": "Suspicious Keywords",
                "value": features[13],
                "reason": "Multiple suspicious keywords may indicate phishing attempt",
                "severity": "high" if features[13] > 4 else "medium"
            })
        
        # Check for @ symbol (often used in phishing)
        if features[16] > 0:  # @ symbol present
            concerns.append({
                "feature": "@ Symbol",
                "value": "Present",
                "reason": "@ symbol in URL can be used to obfuscate the real domain",
                "severity": "high"
            })
        
        # Check for unusual ports
        if features[17] > 0:  # Unusual port present
            concerns.append({
                "feature": "Unusual Port",
                "value": "Present",
                "reason": "Non-standard ports may indicate malicious activity",
                "severity": "medium"
            })
        
        # Check for many parameters
        if features[15] > 5:  # Parameter count
            concerns.append({
                "feature": "Parameter Count",
                "value": features[15],
                "reason": "Excessive parameters may indicate obfuscation or tracking",
                "severity": "medium" if features[15] > 10 else "low"
            })
        
        # Generate human-readable explanation
        text_explanation = self._generate_url_text_explanation(url, features)
        
        return {
            "url_analysis": {
                "features": {name: value for name, value in zip(feature_names, features)},
                "concerns": concerns,
                "text_explanation": text_explanation,
                "feature_importance": feature_importance
            }
        }
    
    def _generate_url_text_explanation(self, url: str, features: List[float]) -> List[str]:
        """Generate human-readable explanations for URL analysis."""
        explanations = []
        
        # Parse URL for additional context
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        
        # Check domain characteristics
        if '.' in domain:
            parts = domain.split('.')
            if len(parts) > 3:
                explanations.append("Domain has many subdomains, which can be used to appear legitimate")
        
        # Check for suspicious TLDs (simplified list)
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top']
        for tld in suspicious_tlds:
            if url.endswith(tld):
                explanations.append(f"Uses '{tld}' top-level domain, often associated with suspicious sites")
                break
        
        # Check path characteristics
        if len(path) > 50:
            explanations.append("Unusually long path in URL, may contain obfuscated content")
        
        # Check for common phishing patterns
        if 'login' in url.lower() or 'secure' in url.lower() or 'account' in url.lower():
            explanations.append("Contains terms commonly used in phishing attempts")
        
        # If no specific patterns found, provide general explanation
        if not explanations:
            explanations.append("Based on machine learning analysis of URL structure and patterns")
        
        return explanations