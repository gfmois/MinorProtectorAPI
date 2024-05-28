import tensorflow as tf
from src.model.metrics import F1Score, Specificity

class AgeClassifier:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        """
        Load the model from a .h5 file.
        """
        try:
            model = tf.keras.models.load_model(model_path, custom_objects={
                'Specificity': Specificity,
                'F1Score': F1Score 
            })
            print("Model loaded successfully.")
            return model
        except Exception as e:
            raise Exception(f"Error loading model: {e}")

    def predict(self, input_data):
        """
        Make a prediction using the loaded model.
        """
        if self.model is not None:
            try:
                prediction = self.model.predict(input_data)
                return prediction
            except Exception as e:
                print(f"Error making prediction: {e}")
                return None
        else:
            raise Exception("Model is not loaded.")