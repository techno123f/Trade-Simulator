# models/slippage_model.py
from sklearn.linear_model import LinearRegression

class SlippageEstimator:
    def __init__(self):
        self.model = LinearRegression()
    
    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, order_size, spread, volatility):
        return self.model.predict([[order_size, spread, volatility]])[0]
