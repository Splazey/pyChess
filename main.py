import threading
import queue
import pygame
import board
from highlighter import Highlighter
import pyaudio
from faster_whisper import WhisperModel
import wave
import os
from ChessTimer import ChessTimer

SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 900
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"

model_size = "small" # TODO must be large-v3
model = WhisperModel(model_size, device="cpu", compute_type="int8")

print("model loading done")

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

timer = ChessTimer(usertime=600.0)  # Timer for 10 minutes per player
font = pygame.font.SysFont("DS-Digital", 40)  # Pygame font for displaying the timer

# Main game loop
while running:
    b.blitBoard()  # render the board itself

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Get the x and y coordinates of the click
            if b.movePiece(x, y, turn, 'coordinate'):
                timer.switch_user()  # Switch user when a move is made
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

    # Draw the timers
    white_time, black_time = timer.get_times()
    white_timer_surface = font.render(f"{white_time}", True, (255, 255, 255))
    black_timer_surface = font.render(f"{black_time}", True, (255, 255, 255))

    # Coordinates for the timers
    black_timer_y = 130  # Position User 2 timer at the top of the board
    white_timer_y = SCREEN_HEIGHT - 165  # Position User 1 timer at the bottom of the board

    # Blit the timers to their new positions
    screen.blit(black_timer_surface, (970 - black_timer_surface.get_width() // 2, black_timer_y))  # Top center for Black
    screen.blit(white_timer_surface, (970- white_timer_surface.get_width() // 2, white_timer_y))  # Bottom center for White

    # Check for timeout
    if timer.is_game_over():
        print("Game Over: Time's Up!")
        running = False
        
    b.renderHighlights()  # render the highlights made by the board
    b.renderPieces()  # render the pieces stored in the board
    pygame.display.update()  # Update the display

pygame.quit()
p.terminate()
