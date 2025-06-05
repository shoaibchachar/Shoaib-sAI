from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import uuid
import os

app = Flask(__name__)

# Load the Urdu model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False)

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    file_path = f"{uuid.uuid4()}.wav"
    tts.tts_to_file(
        text=text,
        file_path=file_path,
        speaker_idx=0,
        language="ur"
    )

    # Return the file first
    response = send_file(file_path, mimetype='audio/wav')

    # Then delete it after sending
    @response.call_on_close
    def cleanup():
        try:
            os.remove(file_path)
        except:
            pass

    return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)
