from flask import Flask, request, jsonify, render_template
import base64
import pyttsx3

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/texttospeech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')
    voice_type = data.get('voice', 'male')  # 'male' or 'female'
    speed = data.get('speed', 150)  # default speed

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    if voice_type == 'female':
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)

    # Set the speed
    engine.setProperty('rate', speed)

    # Generate speech
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

    # Read the generated audio file and convert it to base64
    with open("output.mp3", 'rb') as file:
        audio_bytes = file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

    return jsonify({'audio_base64': audio_base64})

if __name__ == '__main__':
    app.run(debug=True)
