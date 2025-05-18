# # main.py
# from data.websocket_client import stream_orderbook
# from models import slippage_model, market_impact_model

# async def process_tick(data, latency):
#     bids = data['bids']
#     asks = data['asks']
#     spread = float(asks[0][0]) - float(bids[0][0])
    
#     # Inputs
#     order_size = 100  # USD equivalent
#     volatility = 0.03  # Example
#     # Example implementation of get_fee function
#     def get_fee(order_type):
#         if order_type == "market":
#             return 0.001  # Example market fee
#         elif order_type == "limit":
#             return 0.0005  # Example limit fee
#         else:
#             return 0.0

#     fee = get_fee("market")
    
#     slippage = slippage_model.predict(order_size, spread, volatility)
#     impact = market_impact_model.almgren_chriss_impact(order_size, volatility)
#     cost = slippage + (order_size * fee) + impact

#     # Update UI with results
#     print({
#         "slippage": slippage,
#         "impact": impact,
#         "fees": fee * order_size,
#         "net_cost": cost,
#         "latency": latency
#     })

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(stream_orderbook(process_tick))


# main.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox
from trade.data.websocket_client import WebSocketClient
from PyQt5.QtCore import QTimer, pyqtSignal, QObject

class DataHandler(QObject):
    data_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

class TradeSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Trade Simulator - OKX")
        self.setGeometry(100, 100, 700, 400)

        self.output_fields = {}
        self.data_handler = DataHandler()
        self.data_handler.data_received.connect(self.update_outputs)

        self.init_ui()
        self.client = WebSocketClient(on_message_callback=self.process_orderbook)
        self.client.start()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left Panel - Inputs
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Exchange: OKX"))
        input_layout.addWidget(QLabel("Asset: BTC-USDT-SWAP"))
        input_layout.addWidget(QLabel("Order Type: Market"))
        self.quantity_input = QLineEdit("100")
        input_layout.addWidget(QLabel("Quantity (USD):"))
        input_layout.addWidget(self.quantity_input)
        self.volatility_input = QLineEdit("0.02")
        input_layout.addWidget(QLabel("Volatility:"))
        input_layout.addWidget(self.volatility_input)
        self.fee_input = QLineEdit("0.001")
        input_layout.addWidget(QLabel("Fee Tier:"))
        input_layout.addWidget(self.fee_input)
        simulate_btn = QPushButton("Start Simulation")
        simulate_btn.clicked.connect(self.start_simulation)
        input_layout.addWidget(simulate_btn)

        # Right Panel - Outputs
        output_layout = QVBoxLayout()
        for field in [
            "Expected Slippage", "Expected Fees", "Market Impact",
            "Net Cost", "Maker/ Taker Proportion", "Internal Latency"
        ]:
            label = QLabel(f"{field}:")
            value = QLabel("...")
            self.output_fields[field] = value
            output_layout.addWidget(label)
            output_layout.addWidget(value)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        self.setLayout(main_layout)

    def process_orderbook(self, data):
        # Here, do some computations with the orderbook
        # For now, just forward to UI thread
        self.data_handler.data_received.emit(data)

    def update_outputs(self, data):
        import time
        start_time = time.time()

        bids = data.get("bids", [])
        asks = data.get("asks", [])
        if not bids or not asks:
            return

        mid_price = (float(bids[0][0]) + float(asks[0][0])) / 2
        quantity_usd = float(self.quantity_input.text())
        fee_rate = float(self.fee_input.text())

        expected_slippage = 0.03  # dummy %
        fees = quantity_usd * fee_rate
        impact = 0.005 * quantity_usd  # Almgren-Chriss dummy
        net_cost = fees + impact + expected_slippage

        self.output_fields["Expected Slippage"].setText(f"{expected_slippage:.3f}%")
        self.output_fields["Expected Fees"].setText(f"${fees:.2f}")
        self.output_fields["Market Impact"].setText(f"${impact:.2f}")
        self.output_fields["Net Cost"].setText(f"${net_cost:.2f}")
        self.output_fields["Maker/ Taker Proportion"].setText("60% / 40%")
        self.output_fields["Internal Latency"].setText(f"{(time.time() - start_time) * 1000:.1f} ms")

    def start_simulation(self):
        # Just trigger dummy update for now
        print("[INFO] Manual simulation start triggered.")

app = QApplication(sys.argv)
simulator = TradeSimulator()
simulator.show()
sys.exit(app.exec_())

