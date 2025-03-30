import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences

class JobPredictionService:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.model = None
        self.tokenizer = None
        self.scaler = None
        self.config = None
        self.load_model_artifacts()
    
    def load_model_artifacts(self):
        """Load model and preprocessing artifacts from disk"""
        try:
            # Load model
            model_path = os.path.join(self.model_dir, 'fake_job_detection_model.keras')
            self.model = keras.models.load_model(model_path)
            
            # Load tokenizer
            tokenizer_path = os.path.join(self.model_dir, 'tokenizer.pickle')
            with open(tokenizer_path, 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            
            # Load scaler
            scaler_path = os.path.join(self.model_dir, 'salary_scaler.pickle')
            with open(scaler_path, 'rb') as handle:
                self.scaler = pickle.load(handle)
            
            # Load config
            config_path = os.path.join(self.model_dir, 'model_config.json')
            with open(config_path, 'r') as f:
                import json
                self.config = json.load(f)
            
            print("Model and related artifacts loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model artifacts: {str(e)}")
            return False
    
    def predict(self, job_data):
        """
        Make predictions on job data
        
        Args:
            job_data (dict): Dictionary containing job listing data with keys:
                - title: job title
                - company_profile: company information
                - description: job description
                - requirements: job requirements
                - benefits: job benefits (optional)
                - salary: salary value
                
        Returns:
            dict: Prediction results with fraud probability
        """
        if not self.model or not self.tokenizer or not self.scaler or not self.config:
            return {"error": "Model not loaded", "fraud_probability": None}
        
        try:
            # Prepare text data
            combined_text = f"{job_data.get('title', '')} {job_data.get('company', '')} {job_data.get('description', '')} {job_data.get('requirements', '')} {job_data.get('benefits', '')}"
            
            # Tokenize and pad
            sequences = self.tokenizer.texts_to_sequences([combined_text])
            X_text = pad_sequences(sequences, maxlen=self.config.get('MAX_LEN', 300))
            
            # Scale salary
            try:
                salary = float(job_data.get('salary', 0))
            except (ValueError, TypeError):
                salary = 0
                
            X_salary = self.scaler.transform([[salary]])
            
            # Make prediction
            prediction = self.model.predict([X_text, X_salary])
            fraud_probability = float(prediction[0][0])
            
            # Convert to percentage
            fraud_probability_percentage = fraud_probability * 100
            legitimacy_score = 100 - fraud_probability_percentage
            
            return {
                "fraud_probability": fraud_probability,
                "fraud_probability_percentage": fraud_probability_percentage,
                "legitimacy_score": round(legitimacy_score, 1)
            }
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return {"error": str(e), "fraud_probability": None}