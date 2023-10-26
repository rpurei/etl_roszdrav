from flaskapp import create_app
from flaskapp.config import APP_PORT, APP_HOST
from flask_socketio import SocketIO, join_room
from flask import request, session

socket_io = None
app = create_app()
if app:
    socket_io = SocketIO(app, logger=True, engineio_logger=True, message_queue='redis://redis:6379')
else:
    exit(-99)


@socket_io.on('connect', namespace='/runAsyncTaskF')
def socket_connect():
    print('Client Connected To NameSpace /runAsyncTaskF - ', request.sid)


@socket_io.on('disconnect', namespace='/runAsyncTaskF')
def socket_connect():
    print('Client disconnected From NameSpace /runAsyncTaskF - ', request.sid)


@socket_io.on('join_room', namespace='/runAsyncTaskF')
def on_room():
    room = str(session['uid'])
    print(f'Socket joining room {room}')
    join_room(room)


@socket_io.on_error_default
def error_handler(e):
    print(f'Socket error: {e}, {str(request.event)}')


if __name__ == '__main__':
    socket_io.run(app, debug=True, host=APP_HOST, port=APP_PORT)
