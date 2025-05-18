# models/maker_taker_model.py
from sklearn.linear_model import LogisticRegression

class MakerTakerModel:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, spread, order_size):
        return self.model.predict_proba([[spread, order_size]])[0]
