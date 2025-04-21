from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio_stream')
def handle_audio_stream(data):
    # Receives audio stream from client
    audio_data = base64.b64decode(data)
    # Here you can process the audio data or forward it to a speaker
    emit('play_audio', data, broadcast=True)  # Broadcast to other clients

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)