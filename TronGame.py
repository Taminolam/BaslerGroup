import keyboard
import pygame
try:
    import DasSpiel as BAPI
except ImportError:
    import DasSpielSimulation as BAPI
# BAPI may stand for "Basler API" :-)
from Ball import Ball
import GameSounds
from GameHelper import calcDistance
from LightCycle import LightCycle
from LightCycleTrail import LightCycleTrail
import Config as Cfg
import math


# Script entry function.
# It runs a Basler version of the classic computer game TRON.
def main():
    mainWindow = initMainWindow("Tron", Cfg.MAIN_WINDOW_WIDTH_PX, Cfg.MAIN_WINDOW_HEIGHT_PX)
    standingItems = mainWindow.standingItemsManager
    lyingItems = mainWindow.lyingItemsManager
    #<blau>fostenlinks (300,=tiefe 600=breite))
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(300, 380))
    #<blau>fostenrechts
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(300, 825))
    #<blau>fostenhintenlinks
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(10, 380))
    #<blau>fostenhintenrechts
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(10, 825))
    #<blau>latte
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\deineLatte.png"), BAPI.Point(300, 600))
    #<orange>
    #<orange>fostenlinks
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(1500, 825))
    #<orange>fostenrechts
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(1500, 380))
    #<orange>latte
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\deineLatte.png"), BAPI.Point(1500, 600))
     #<orange>fostenhintenlinks
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(1780, 825))
    #<orange>fostenhintenrechts
    standingingItems = mainWindow.standingItemsManager
    standingingItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\fosten.png"), BAPI.Point(1780, 380))
    # the item manager for head up displays
    frontItems = mainWindow.frontItemsManager
    frontItems.createAndAddItem(BAPI.loadImage(".\\Bilder\\Basler_Tron.png"), BAPI.Point(320, 5))
    # set the field ground image in simulation mode
    background = BAPI.loadcvImage(".\\Bilder\\Basler_Spielfeld.png")
    BAPI.setImage4NoCameraMode(background)
    lightCycles = initLightCycles()

    # one grab and calculation to determine the cars positions and angles
    img = BAPI.grabFromCamera()
    mainWindow.asyncHandleCarsAndBackground(img)
    mainWindow.wait4Asyncs()
    for bike in lightCycles:
        bike.setAngleIdToClosestMatchingAngle()

    trails = initBikeTrails(lyingItems, lightCycles)

    views = initViews(mainWindow, lightCycles)
    
    ball = Ball (BAPI.Point(900, 600),standingItems)
    
    GameSounds.playsound1Sound()
    GameSounds.playsound2Sound()
    GameSounds.playsound3Sound()
#neue sounds
    while True:
        # Basic game API code
        img = BAPI.grabFromCamera()
        #mainWindow.asyncHandleCarsAndBackground(img)
        #mainWindow.wait4Asyncs()
        mainWindow.searchCars(img)
        mainWindow.calcBackground(background)

        # Views need to be adapted here to create a smooth animation!
        adaptViewsToFollowBikes(lightCycles, views)

        # Basic game API code
        mainWindow.asyncCalcViews()
        mainWindow.wait4Asyncs()
        mainWindow.calcFront()
        mainWindow.display()

        if keyboard.is_pressed('q'):
            # quit the game!
            mainWindow.close()
            GameSounds.uninit()
            break;
        elif keyboard.is_pressed('r'):
            # reset the game!
            for item in lyingItems.getListOfItems():
                lyingItems.removeItem(item)
            lightCycles = initLightCycles()
            trails = initBikeTrails(lyingItems, lightCycles)
            ball._position = BAPI.Point(900,600) 
            ball.speed = 0
            GameSounds.stopSoundPlayback()
            GameSounds.playsound1Sound()
            GameSounds.playsound2Sound()
            GameSounds.playsound3Sound()

        # bike ans biketrail behaviour
        for bike, bikeTrail in zip(lightCycles, trails):
            bike.handleSteeringInputs()
            bike.controlSteeringAngle()
            bikeTrail.generate(bike)

        handleCollisionOfLightCyclesAndTrails(Cfg.COLLISION_DISTANCE_LIMIT_TRAILS_PX, lightCycles, trails)
        handleCollisionOfLightCyclesWithEachOther(Cfg.COLLISION_DISTANCE_LIMIT_LIGHTCYCLES_PX, lightCycles)
        handleCollisionOfLightCyclesWithBoundaries(Cfg.COLLISION_DISTANCE_LIMIT_FIELD_BOUNDARIES_PX,
                                                   Cfg.FIELD_WIDTH_PX,
                                                   Cfg.FIELD_HEIGHT_PX,
                                                   lightCycles)
        handleCollisonOfBall(lightCycles, ball)

        ball.update()

def initMainWindow(name, fieldWidthPx, fieldHeightPx):
    mainWindow = BAPI.getWindow()
    mainWindow.setSize(fieldWidthPx, fieldHeightPx)
    mainWindow.name = name
    mainWindow.showFPS = True
    return mainWindow


def initLightCycles():
    bike0Keys = {'forwardKey':'w',
             'backwardKey':'s',
             'turnLeftKey':'a',
             'turnRightKey':'d',
             'specialAbilityKey':'e', 
             'specialRoundKey':'f',}
             
    bike0 = LightCycle(0, bike0Keys, BAPI.Point(1650, 600), 4)
#bike0=rotes bike
    bike1Keys = {'forwardKey':'i',
                 'backwardKey':'k',
                 'turnLeftKey':'j',
                 'turnRightKey':'l',
                 'specialAbilityKey':'o',
                 'specialRoundKey':'ö',}
                
    bike1 = LightCycle(1, bike1Keys, BAPI.Point(120, 600), 0)
#bike1=blaues bike(100
    bikes = (bike0, bike1)

    return bikes


def initBikeTrails(graphicsObjectManager, bikes):
    bike0trail = LightCycleTrail(graphicsObjectManager, bikes[0])
    bike1trail = LightCycleTrail(graphicsObjectManager, bikes[1])
    return (bike0trail, bike1trail)


def  handleCollisionOfLightCyclesAndTrails(distanceLimitPx, lightCycles, trails):
    # collision with light cycle trails trail
    for trail in trails:
        collisions = trail.getCollidedObjects(lightCycles, distanceLimitPx)
        if len(collisions) > 0:
            for collision in collisions:
                lightCycles[collision[0]._carId].destroy()
                
def handleCollisonOfBall (cars,ball):
    for car in cars: 
        
        if calcDistance(ball._position, car._car.position) <= 40:
            ball.shoot(-car._car.angle + math.pi/2, car._car.throttle*10)              
    if ball._position.x <=0 or ball._position.x >=1200 or ball._position.y <=0 or ball._position.y >=1800: 
        ball._position = BAPI.Point (900,600)      
        ball.speed = 0    
def handleCollisionOfLightCyclesWithEachOther(distanceLimitPx, lightCycles):
    # collision lightCycles with each other
    if calcDistance(lightCycles[0].getPosition(), lightCycles[1].getPosition()) < distanceLimitPx:
        for bike in lightCycles:
            bike.destroy()


def handleCollisionOfLightCyclesWithBoundaries(distanceLimitPx, fieldWidthPx, fieldHeightPx, lightCycles):
    # collision with field boundaries
    distanceLimitForFieldLimitsPx = distanceLimitPx // 4
    for bike in lightCycles:
        position = bike.getPosition()
        if (position.x < distanceLimitForFieldLimitsPx
            or position.x > (fieldWidthPx - distanceLimitForFieldLimitsPx)
            or position.y < distanceLimitForFieldLimitsPx
            or position.y > (fieldHeightPx - distanceLimitForFieldLimitsPx)):
            pass #bike.destroy()


def adaptViewsToFollowBikes(bikes, views):
    for bike, view in zip(bikes, views):
        view.setViewFromCar(bike.getCarObject())


def initViews(mainWindow, bikes):
    views = []
    view = mainWindow.createView(mainWindow.width // 2, mainWindow.height, 2, 0)
    views.append(view)
    view = mainWindow.createView(mainWindow.width // 2, mainWindow.height, mainWindow.width // 2, 0)
    views.append(view)
    for bike, view in zip(bikes, views):
        view.showLyingItems = True
        view.showStandingItems = True
        view.setViewFromCar(bike.getCarObject())  # attach view to the diretion/angle of a bike
    return views




###########################################
###########################################
###########################################
if __name__ == '__main__':
    main()


