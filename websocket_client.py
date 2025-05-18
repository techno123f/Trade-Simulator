# # data/websocket_client.py

# import asyncio
# import websockets
# import json
# from datetime import datetime
# import logging

# async def stream_orderbook(callback):
#     uri = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             start = datetime.now()
#             message = await websocket.recv()
#             end = datetime.now()
#             latency = (end - start).total_seconds()
#             data = json.loads(message)
#             await callback(data, latency)


# trade/data/websocket_client.py
import websocket
import json
import threading

class WebSocketClient:
    def __init__(self, symbol="BTC-USDT-SWAP", on_message_callback=None):
        self.ws_url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{symbol}"
        self.ws = None
        self.running = False
        self.on_message_callback = on_message_callback

    def _on_message(self, ws, message):
        data = json.loads(message)
        if self.on_message_callback:
            self.on_message_callback(data)

    def _on_error(self, ws, error):
        print("[ERROR]", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("[INFO] WebSocket closed")

    def _on_open(self, ws):
        print("[INFO] WebSocket connection opened")

    def start(self):
        self.running = True
        def run():
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )
            self.ws.run_forever()
        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()
