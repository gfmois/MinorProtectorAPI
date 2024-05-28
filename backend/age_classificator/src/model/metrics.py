import tensorflow as tf
from tensorflow.keras.metrics import Precision, Recall

# Custom Specificity
class Specificity(tf.keras.metrics.Metric):
    def __init__(self, name='specificity', **kwargs):
        super(Specificity, self).__init__(name=name, **kwargs)
        self.true_negatives = self.add_weight(name='tn', initializer='zeros')
        self.false_positives = self.add_weight(name='fp', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.cast(y_true, tf.bool)
        y_pred = tf.cast(y_pred > 0.5, tf.bool)
        self.true_negatives.assign_add(tf.reduce_sum(
            tf.cast(tf.logical_not(y_true) & tf.logical_not(y_pred), tf.float32)))
        self.false_positives.assign_add(tf.reduce_sum(
            tf.cast(tf.logical_not(y_true) & y_pred, tf.float32)))

    def result(self):
        specificity = self.true_negatives / \
            (self.true_negatives + self.false_positives)
        return specificity

    def reset_state(self):
        self.true_negatives.assign(0)
        self.false_positives.assign(0)

# Definir la métrica F1-Score
class F1Score(tf.keras.metrics.Metric):
    def __init__(self, name='f1_score', **kwargs):
        super(F1Score, self).__init__(name=name, **kwargs)
        self.precision = Precision()
        self.recall = Recall()

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.precision.update_state(y_true, y_pred, sample_weight)
        self.recall.update_state(y_true, y_pred, sample_weight)

    def result(self):
        p = self.precision.result()
        r = self.recall.result()
        return 2 * ((p * r) / (p + r + tf.keras.backend.epsilon()))

    def reset_states(self):
        self.precision.reset_state()
        self.recall.reset_state()

