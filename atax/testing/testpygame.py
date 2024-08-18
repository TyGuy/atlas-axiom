import pygame
import time

def test_pygame_audio():
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        print("Pygame mixer initialized.")

        # Load a sample audio file
        pygame.mixer.music.load('test.wav')  # Replace 'test.wav' with your file path
        print("Audio file loaded.")

        # Play the audio file
        pygame.mixer.music.play()
        print("Audio playback started.")

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Check every 100 milliseconds

        print("Audio playback finished.")
    
    except pygame.error as e:
        print(f"Pygame error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Clean up pygame mixer
        pygame.mixer.quit()
        print("Pygame mixer quit.")

if __name__ == "__main__":
    test_pygame_audio()
