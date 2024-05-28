from src.model.age_classifier import AgeClassifier

class AgeClassifierService:
    def __init__(self, model_path):
        """
        Initialize the AgeClassifier model.
        """
        self.classifier = AgeClassifier(model_path)

    def make_prediction(self, input_data):
        """
        Use the classifier to make a prediction based on the input data.
        """
        return self.classifier.predict(input_data)