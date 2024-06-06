import websocket

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")

def run():
    ws = websocket.WebSocketApp(
        "ws://localhost:8002/socket.io",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    # Chạy mãi mãi để giữ kết nối và xử lý tin nhắn
    ws.run_forever()

if __name__ == "__main__":
    run()
