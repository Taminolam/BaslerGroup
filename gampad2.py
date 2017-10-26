import time
import pygame

def main():
    pygame.init()
   
    joysticks = list()
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
   
    while True:
        pygame.event.pump()
        for joystick in joysticks:
            print ('Count: %d Axis0: %s Axis1: %s Button0: %s'
                   % (len(joysticks),
                      joystick.get_axis(3),
                      joystick.get_axis(4),
                      joystick.get_button(0)))
        time.sleep(1)
main()