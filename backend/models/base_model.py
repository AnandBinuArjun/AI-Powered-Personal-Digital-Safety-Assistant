from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np

class BaseModel(ABC):
    """Abstract base class for all ML models."""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        # Don't call load_model here to avoid issues during initialization
        # self.load_model()
    
    @abstractmethod
    def load_model(self):
        """Load the model from disk."""
        pass
    
    @abstractmethod
    def preprocess(self, data: str) -> Any:
        """Preprocess input data for the model."""
        pass
    
    @abstractmethod
    def predict(self, data: str) -> Dict[str, Any]:
        """Make a prediction on the input data."""
        pass
    
    @abstractmethod
    def explain_prediction(self, data: str) -> Dict[str, Any]:
        """Provide explanation for the prediction."""
        pass
    
    def get_confidence(self, prediction_proba: np.ndarray) -> float:
        """Extract confidence score from prediction probabilities."""
        if len(prediction_proba.shape) == 1:
            return float(np.max(prediction_proba))
        else:
            return float(np.max(prediction_proba, axis=1)[0])