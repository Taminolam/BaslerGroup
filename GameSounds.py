import pygame as pg


pg.mixer.init()

__GRID_LIVE_SOUND = pg.mixer.Sound("Sounds\grid_is_live.wav")
__LIGHTCYCLE_SOUND = pg.mixer.Sound("Sounds\lightcycle.wav")
__SOUND1_SOUND = pg.mixer.Sound("Sounds\sound1.wav")
__SOUND2_SOUND = pg.mixer.Sound("Sounds\sound2.wav")
__SOUND3_SOUND = pg.mixer.Sound("Sounds\sound3.wav")
def playGridIsLiveSound():
    __GRID_LIVE_SOUND.play()


def playLightCycleSound():
    __LIGHTCYCLE_SOUND.play()

def uninit():
    pg.mixer.quit()

def stopSoundPlayback():
    pg.mixer.stop()

def playsound1Sound():
    __SOUND1_SOUND.play()
    
def playsound2Sound():
    __SOUND2_SOUND.play()

def playsound3Sound():
    __SOUND3_SOUND.play()
    
    