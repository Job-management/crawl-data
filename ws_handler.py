# websocket_handler.py
import socketio

# Create a Socket.IO server with ASGI
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# Define the event handlers
from status_handler import StatusHandler

# Initialize the status handler
status_handler = StatusHandler()

@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)
    await sio.emit('broadcast', "Connected", to=sid)

@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
async def current_status(sid):
    await sio.emit('current_status', status_handler.get_status(), to=sid)
    print('current_status:', sid)

# Create the ASGI application for Socket.IO
socket_app = socketio.ASGIApp(sio, socketio_path='/socket.io')
