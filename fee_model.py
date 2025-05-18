# utils/fee_model.py
def get_fee(order_type, tier="default"):
    if order_type == "market":
        return 0.001  # Example: 0.1%
    return 0.0005
