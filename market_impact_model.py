# models/market_impact_model.py
def almgren_chriss_impact(order_size, volatility, gamma=0.1, eta=0.05):
    """
    Returns estimated permanent + temporary impact using Almgren-Chriss simplified model.
    """
    permanent = gamma * order_size
    temporary = eta * (order_size ** 0.5)
    return permanent + temporary
