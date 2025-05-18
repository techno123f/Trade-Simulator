


from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFormLayout, QGroupBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import sys
import datetime

class TradeSimulatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("High-Performance Trade Simulator")
        self.setGeometry(100, 100, 800, 400)

        main_layout = QHBoxLayout(self)

        # Left Panel: Input Parameters
        input_group = QGroupBox("Input Parameters")
        input_layout = QFormLayout()

        # Exchange dropdown (only OKX for now)
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(["OKX"])
        input_layout.addRow(QLabel("Exchange:"), self.exchange_combo)

        # Spot Asset dropdown - sample assets, could be dynamically loaded later
        self.asset_combo = QComboBox()
        self.asset_combo.addItems(["BTC-USDT-SWAP", "ETH-USDT-SWAP", "LTC-USDT-SWAP"])
        input_layout.addRow(QLabel("Spot Asset:"), self.asset_combo)

        # Order Type (fixed 'market' as per requirement)
        self.order_type_label = QLabel("market")
        input_layout.addRow(QLabel("Order Type:"), self.order_type_label)

        # Quantity with numeric validator (~100 USD equivalent)
        self.quantity_input = QLineEdit("100")
        self.quantity_input.setValidator(QDoubleValidator(0.01, 1000000, 8))
        input_layout.addRow(QLabel("Quantity (USD):"), self.quantity_input)

        # Volatility input (numeric)
        self.volatility_input = QLineEdit("0.05")  # example default 5%
        self.volatility_input.setValidator(QDoubleValidator(0.0, 10.0, 5))
        input_layout.addRow(QLabel("Volatility:"), self.volatility_input)

        # Fee Tier input (numeric, integer)
        self.fee_tier_input = QLineEdit("1")
        self.fee_tier_input.setValidator(QIntValidator(1, 10))
        input_layout.addRow(QLabel("Fee Tier:"), self.fee_tier_input)

        # Start and Stop Buttons
        self.start_button = QPushButton("Start Simulation")
        self.stop_button = QPushButton("Stop Simulation")
        self.stop_button.setEnabled(False)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        input_layout.addRow(btn_layout)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group, 1)

        # Right Panel: Output Parameters
        output_group = QGroupBox("Output Parameters")
        output_layout = QFormLayout()

        self.output_fields = {}
        output_names = [
            "Expected Slippage",
            "Expected Fees",
            "Market Impact",
            "Net Cost",
            "Maker/ Taker Proportion",
            "Internal Latency"
        ]

        for name in output_names:
            label = QLabel("N/A")
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            output_layout.addRow(QLabel(name + ":"), label)
            self.output_fields[name] = label

        # Connection Status Label
        self.connection_status = QLabel("Disconnected")
        self.connection_status.setStyleSheet("color: red; font-weight: bold;")
        output_layout.addRow(QLabel("Connection Status:"), self.connection_status)

        # Last Updated Label
        self.last_updated = QLabel("Never")
        output_layout.addRow(QLabel("Last Updated:"), self.last_updated)

        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group, 1)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button.clicked.connect(self.stop_simulation)

        # Timer for demo update (remove when hooking to real WS)
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self.update_demo_outputs)

    def start_simulation(self):
        # Disable start, enable stop
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # Set connection status
        self.connection_status.setText("Connected")
        self.connection_status.setStyleSheet("color: green; font-weight: bold;")

        # Start demo timer (simulate real-time updates)
        self.demo_timer.start(1000)  # every 1 second

    def stop_simulation(self):
        # Enable start, disable stop
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        # Set connection status
        self.connection_status.setText("Disconnected")
        self.connection_status.setStyleSheet("color: red; font-weight: bold;")

        # Stop demo timer
        self.demo_timer.stop()

        # Reset outputs
        for label in self.output_fields.values():
            label.setText("N/A")
        self.last_updated.setText("Never")

    def update_demo_outputs(self):
        # This function would be replaced with real-time data processing updates
        import random

        self.output_fields["Expected Slippage"].setText(f"{random.uniform(0.02, 0.05):.3%}")
        self.output_fields["Expected Fees"].setText(f"${random.uniform(0.05, 0.15):.2f}")
        self.output_fields["Market Impact"].setText(f"${random.uniform(0.4, 0.7):.2f}")
        net_cost = sum(
            float(self.output_fields[name].text().replace('$', '').replace('%', '')) 
            for name in ["Expected Slippage", "Expected Fees", "Market Impact"]
        )
        self.output_fields["Net Cost"].setText(f"${net_cost:.2f}")
        maker_pct = random.randint(40, 70)
        taker_pct = 100 - maker_pct
        self.output_fields["Maker/ Taker Proportion"].setText(f"{maker_pct}% / {taker_pct}%")
        self.output_fields["Internal Latency"].setText(f"{random.uniform(1.5, 2.5):.1f} ms")
        self.last_updated.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradeSimulatorUI()
    window.show()
    sys.exit(app.exec())
