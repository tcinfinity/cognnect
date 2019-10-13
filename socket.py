from flask_socketio import SocketIO

socketio = SocketIO(app)

@app.route('/chat/<uuid>', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')

@socketio.on('connect')

# run flask app this way for socketio (chat)
# better to allow for SocketIO to have WebSocket support ()
if __name__ == '__main__':
    socketio.run(app)