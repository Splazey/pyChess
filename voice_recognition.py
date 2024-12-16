import pyaudio
from faster_whisper import WhisperModel
import wave
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"

model_size = "large-v3"
# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
channels=CHANNELS,
rate=RATE,
input=True,
frames_per_buffer=CHUNK)

print("* recording")

while True:
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    segments, info = model.transcribe(WAVE_OUTPUT_FILENAME, beam_size=5, language="en", condition_on_previous_text=False)

    # for segment in segments:
    #     print(segments.start)
    #     print(segments.end)
    #     print(segments.text)

    for segment in segments:
        s =  segment.text
        print(s)