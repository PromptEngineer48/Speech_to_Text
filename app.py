import pyaudio
import wave
from huggingsound import SpeechRecognitionModel

## Record audio from the microphone # created using ChatGPT
def record_audio(duration, output_file):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording started. Speak into the microphone...")
    frames = []
    # Record audio for the specified duration
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    # print("Recording completed.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save the recorded audio as a .wav file
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english
def speech_recognizer(audio_input):
    model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")
    audio_paths = [audio_input]
    transcriptions = model.transcribe(audio_paths)
    return transcriptions[0]['transcription']

def main():
    record_audio(5, 'audio.mp3' )
    output = speech_recognizer('audio.mp3')
    print(output)
    
if __name__ == "__main__":
    main()

    