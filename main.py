import threading
import queue
import pygame
import board
from highlighter import Highlighter
import pyaudio
from faster_whisper import WhisperModel
import wave
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"

model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

p = pyaudio.PyAudio()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))  # fill the screen with black color
pygame.display.set_caption("PyChess Project")  # Window title

b = board.Board(screen)
b.setFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")  # FEN code for the chess board position
turn = True

voice_queue = queue.Queue()
running = True

def voice_recognition(): #separate loop to listen for user's voice
    while running:
        # Record audio
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()

        # Save the recording to a file
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


        segments, _ = model.transcribe(WAVE_OUTPUT_FILENAME, beam_size=5, language="en", condition_on_previous_text=False)
        for segment in segments:
            voice_queue.put(segment.text)

# Start the voice recognition thread
listening_thread = threading.Thread(target=voice_recognition, daemon=True)
listening_thread.start()

# Main game loop
while running:
    b.blitBoard()  # render the board itself

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Get the x and y coordinates of the click
            if b.movePiece(x, y, turn, 'coordinate'):
                turn = not turn  # if a piece has been moved, change the turn

    # processing voice input from queue
    while not voice_queue.empty():
        voice_input = voice_queue.get()
        print(f"{voice_input}, length={len(voice_input)}")
        # voice input validation
        if len(voice_input) > 2 and voice_input[1].isalpha() and voice_input[2].isdigit():
            print("-valid input, processing-")
            if b.movePiece(voice_input[1].lower(), voice_input[2], turn, 'character'):
                turn = not turn
        elif len(voice_input) > 3 and voice_input[1].isalpha() and voice_input[3].isdigit():
            print("-valid input, processing-")
            if b.movePiece(voice_input[1].lower(), voice_input[3], turn, 'character'):
                turn = not turn

    b.renderHighlights()  # render the highlights made by the board
    b.renderPieces()  # render the pieces stored in the board
    pygame.display.update()  # Update the display

pygame.quit()
p.terminate()
