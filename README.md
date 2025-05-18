# ⚡ High-Performance Trade Simulator

## 🚀 Overview

This is a real-time crypto trade simulator built with **Python** and **PyQt5**, leveraging **WebSocket** from **OKX Exchange** to fetch real-time Level 2 order book data. The application simulates trade execution, slippage, fees, market impact (via the Almgren-Chriss model), and more — providing a robust interface for users to understand real market execution costs.

---

## 🧱 Architecture Overview

### 🔹 GUI Features (PyQt5)

- **Inputs:**
  - Exchange: OKX
  - Spot Asset: e.g., BTC-USDT-SWAP
  - Order Type: Market
  - Order Quantity (USD)
  - Market Volatility (slider)
  - Fee Tier (1 to 10)

- **Outputs:**
  - Expected Slippage
  - Expected Fees
  - Market Impact (Almgren-Chriss model)
  - Net Cost
  - Maker/Taker Proportion
  - Internal Latency

- **Footer:**
  - WebSocket Connection Status
  - Last Updated Timestamp

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/trade-simulator.git
cd trade-simulator
