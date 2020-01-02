import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print('Recording...')
with mic as source:
    audio = r.listen(source, timeout=1)

    with open("audio_file.wav", "wb") as file:
        file.write(audio.get_wav_data())
