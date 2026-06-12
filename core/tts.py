from gtts import gTTS
import pygame
import os
import time

def speak(text: str, filename="assets/temp_audio/output.mp3"):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)
    
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    time.sleep(0.5)
    
    try:
        os.remove(filename)
    except:
        pass