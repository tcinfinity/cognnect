from flask import Flask, render_template
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijk'
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'hi'

@app.route('/chat/<uuid>', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')


# @socketio.on('connect')
# def onconnect():
#     print()

class ChatSession(Namespace):
    def on_connect(self):
        socket.on()

    def on_disconnect(self):
        pass

    def on_event(self, data):
        pass
        emit()

    def on_client_connect(self, data):
        print(data)

socketio.on_namespace(ChatSession('/chat'))

# run flask app this way for socketio (chat)
# better to allow for SocketIO to have WebSocket support ()
if __name__ == '__main__':
    socketio.run(app, debug=True)