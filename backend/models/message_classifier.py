import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import shap
from typing import Dict, Any
from .base_model import BaseModel

class MessageClassifier(BaseModel):
    """Message classification model for detecting spam/scam messages."""
    
    def __init__(self, model_path: str = "models/message_model.pkl"):
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 2)
        )
        self.label_map = {0: "safe", 1: "suspicious", 2: "scam"}
        self.model = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', MultinomialNB())
        ])
        # Initialize SHAP explainer
        self.explainer = None
    
    def load_model(self):
        """Load the trained model from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            # Initialize a default model if file doesn't exist or is invalid
            self.model = Pipeline([
                ('vectorizer', self.vectorizer),
                ('classifier', MultinomialNB())
            ])
    
    def preprocess(self, message: str) -> str:
        """Preprocess the message text."""
        # Basic preprocessing
        message = message.lower().strip()
        return message
    
    def train(self, messages: list, labels: list):
        """Train the model with provided data."""
        processed_messages = [self.preprocess(msg) for msg in messages]
        self.model.fit(processed_messages, labels)
        
        # Initialize SHAP explainer after training
        # For demonstration, we'll create a simple explainer
        # In production, you would use a proper background dataset
        self._initialize_shap_explainer(processed_messages[:100] if len(processed_messages) > 100 else processed_messages)
        
        # Save the trained model
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def _initialize_shap_explainer(self, background_data: list):
        """Initialize SHAP explainer with background data."""
        try:
            # Create a simple background dataset for SHAP
            if hasattr(self.model.named_steps['classifier'], 'predict_proba'):
                self.explainer = shap.Explainer(
                    self.model.named_steps['classifier'].predict_proba,
                    self.model.named_steps['vectorizer'].transform(background_data)
                )
        except Exception as e:
            print(f"Could not initialize SHAP explainer: {e}")
            self.explainer = None
    
    def predict(self, message: str) -> Dict[str, Any]:
        """Predict if a message is safe, suspicious, or scam."""
        processed_message = self.preprocess(message)
        
        # Get prediction
        prediction = self.model.predict([processed_message])[0]
        
        # Get prediction probabilities
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba([processed_message])[0]
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
    
    def explain_prediction(self, message: str) -> Dict[str, Any]:
        """Provide detailed explanation for the prediction using SHAP and feature importance."""
        try:
            processed_message = self.preprocess(message)
            
            # Get SHAP explanation if available
            shap_explanation = None
            if self.explainer:
                try:
                    # Transform the message
                    message_vector = self.model.named_steps['vectorizer'].transform([processed_message])
                    
                    # Get SHAP values (simplified approach)
                    shap_values = self.explainer(message_vector)
                    shap_explanation = {
                        "shap_values": shap_values.values.tolist() if hasattr(shap_values, 'values') else [],
                        "base_values": shap_values.base_values.tolist() if hasattr(shap_values, 'base_values') else []
                    }
                except Exception as e:
                    print(f"SHAP explanation failed: {e}")
            
            # Get feature names and weights if using a linear model
            feature_explanation = {}
            if hasattr(self.model.named_steps['classifier'], 'coef_'):
                feature_names = self.model.named_steps['vectorizer'].get_feature_names_out()
                coef = self.model.named_steps['classifier'].coef_
                
                # For multiclass, we'll focus on the predicted class
                prediction = self.model.predict([processed_message])[0]
                
                # Get top features for the predicted class
                if len(coef.shape) > 1 and prediction < len(coef):
                    class_coef = coef[prediction]
                elif len(coef.shape) == 1:
                    class_coef = coef
                else:
                    class_coef = np.zeros(len(feature_names))
                
                # Get top positive and negative features
                top_positive_idx = np.argsort(class_coef)[-10:]
                top_negative_idx = np.argsort(class_coef)[:10]
                
                feature_explanation = {
                    "important_words": [
                        {
                            "word": feature_names[i],
                            "weight": float(class_coef[i]),
                            "importance": abs(float(class_coef[i]))
                        } for i in top_positive_idx if class_coef[i] > 0
                    ],
                    "concerning_patterns": [
                        {
                            "pattern": feature_names[i],
                            "weight": float(class_coef[i]),
                            "importance": abs(float(class_coef[i]))
                        } for i in top_negative_idx if class_coef[i] < 0
                    ]
                }
            
            # Text-based explanation
            text_explanation = self._generate_text_explanation(message, processed_message)
            
            explanation = {
                "text_explanation": text_explanation,
                "feature_importance": feature_explanation
            }
            
            if shap_explanation:
                explanation["shap_explanation"] = shap_explanation
                
            return explanation
            
        except Exception as e:
            return {
                "error": f"Could not generate explanation: {str(e)}"
            }
    
    def _generate_text_explanation(self, original_message: str, processed_message: str) -> list:
        """Generate human-readable explanations for the prediction."""
        explanations = []
        
        # Check for common scam patterns
        message_lower = original_message.lower()
        
        if "urgent" in message_lower or "immediate" in message_lower:
            explanations.append("Contains urgent language, often used to pressure victims")
        
        if "click here" in message_lower or "verify account" in message_lower:
            explanations.append("Contains suspicious action prompts")
        
        if "password" in message_lower or "credential" in message_lower:
            explanations.append("Asks for sensitive information")
        
        if "@" in original_message and "." in original_message:
            explanations.append("Contains email-like patterns that may be spoofed")
        
        if len(original_message) > 200:
            explanations.append("Unusually long message, may contain obfuscated content")
        
        # Check for suspicious characters or patterns
        if "!!!" in original_message or "???" in original_message:
            explanations.append("Contains excessive punctuation for emphasis")
        
        if "$" in original_message or "€" in original_message or "£" in original_message:
            explanations.append("Mentions currency, common in financial scams")
        
        # If no specific patterns found, provide general explanation
        if not explanations:
            explanations.append("Based on learned patterns from training data")
        
        return explanations