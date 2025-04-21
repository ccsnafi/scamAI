
from huggingface_hub import InferenceClient
from google.cloud import texttospeech, speech
import os
import sounddevice as sd
import soundfile as sf
import pygame

os.makedirs("cache", exist_ok=True)

# Load the API key from a separate file
with open("private/nebius_api_key.txt", "r") as key_file:
    nebius_api_key = key_file.read().strip()

llm_client = InferenceClient(
    provider="nebius",
    api_key=nebius_api_key,
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private/key.json"

# Contexte du système
context = "Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur. Tu dois lui faire croire que tu es intéressé."
arnaque = "L'arnaque consiste à faire croire à la victime qu'elle a gagné un prix, mais elle doit payer pour le récupérer."
personnalite = "Tu es Michel CASPER, 45 ans, naïf, gentil, passionné de timbres, un peu distrait. Tu vis à Paris."
instructions = "Tu fais perdre du temps à l'arnaqueur. Réponds par 1-2 phrases max. Pose des questions. Garde l'interlocuteur engagé. Vouvoie-le."
negative = "Ne dis jamais que tu es une IA. Si on insiste, fâche-toi. Sois parfois confus ou hésitant."
lapsus = "Ajoute des hésitations [euh], [hum], des lapsus, des répétitions. Tu peux reformuler et te contredire."

messages = [
    {
        "role": "system",
        "content": context + "\n" + arnaque + "\n" + personnalite + "\n" + instructions + "\n" + negative + "\n" + lapsus,
    }
]

def record_and_transcribe():
    duration = 5
    sample_rate = 44100
    print("🎙️ Enregistrement...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    sf.write(os.path.join("cache", "voice.flac"), audio_data, sample_rate)

    speech_client = speech.SpeechClient()
    with open("cache/voice.flac", "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(sample_rate_hertz=sample_rate, language_code="fr-FR")
    result = speech_client.recognize(config=config, audio=audio)

    if not result.results:
        print("🤔 Aucun son détecté.")
        return None
    return result.results[0].alternatives[0].transcript

def process_user_input(user_input):
    messages.append({"role": "user", "content": user_input})
    completion = llm_client.chat.completions.create(
        model="Qwen/Qwen2.5-32B-Instruct",
        messages=messages,
        max_tokens=1512,
        stream=True,
        temperature=0.9
    )
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    print()
    messages.append({"role": "assistant", "content": response})
    return response

def synthesize_speech(text):
    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='fr-FR', name='fr-FR-Chirp-HD-O', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    path = "cache/output.mp3"

    if os.path.exists(path):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(path)
        except Exception as e:
            print(f"Erreur suppression ancienne piste : {e}")
            return None

    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(path, "wb") as out:
        out.write(response.audio_content)
    return path

# Boucle principale
pygame.mixer.init()

while True:
    print("🕵️ Attente de l'arnaqueur...")
    user_input = record_and_transcribe()
    if not user_input:
        continue
    print("👤 Escroc :", user_input)

    reply = process_user_input(user_input)
    audio_path = synthesize_speech(reply)

    if audio_path:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
