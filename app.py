from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
from google.cloud import speech, texttospeech
import os
import tempfile
import base64

app = Flask(__name__)

# Config API Keys
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private/key.json"
with open("private/nebius_api_key.txt", "r") as f:
    api_key = f.read().strip()

llm_client = InferenceClient(provider="nebius", api_key=api_key)

messages = [
    {
        "role": "system",
        "content": (
            "Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur. "
            "Tu es Michel CASPER, 45 ans, passionné de timbres, crédule et distrait. "
            "Réponds par 1-2 phrases max. Pose des questions. Reste naïf mais suspicieux. "
            "Ajoute des hésitations [euh], [hum] et des répétitions. Tu n'es pas une IA."
        ),
    }
]

def transcribe_audio(file_path):
    client = speech.SpeechClient()
    with open(file_path, "rb") as f:
        content = f.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(language_code="fr-FR", sample_rate_hertz=44100)
    result = client.recognize(config=config, audio=audio)
    if result.results:
        return result.results[0].alternatives[0].transcript
    return ""

def generate_reply(user_input):
    messages.append({"role": "user", "content": user_input})
    response = ""
    for chunk in llm_client.chat.completions.create(
        model="Qwen/Qwen2.5-32B-Instruct",
        messages=messages,
        stream=True,
        temperature=0.9
    ):
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    messages.append({"role": "assistant", "content": response})
    return response

def synthesize_speech(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="fr-FR", name="fr-FR-Chirp-HD-O", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=config)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    with open(tmp.name, "wb") as f:
        f.write(response.audio_content)
    return tmp.name

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    audio_data = request.files["audio"]
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_data.save(temp_audio.name)

    text = transcribe_audio(temp_audio.name)
    reply = generate_reply(text)
    voice_file = synthesize_speech(reply)

    with open(voice_file, "rb") as f:
        encoded_voice = base64.b64encode(f.read()).decode("utf-8")

    return jsonify({
        "transcription": text,
        "reply": reply,
        "voice": encoded_voice
    })

if __name__ == "__main__":
    app.run(debug=True)
