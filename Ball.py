from DasSpielSimulation import ItemManager
try:
    import DasSpiel as BAPI
except ImportError:
    import DasSpielSimulation as BAPI
    from DasSpielSimulation import VirtualCar
import time
import math
class Ball():
 
    BALL_STANDARD_IMAGES = (BAPI.loadImage(".\\ball.png"))
 
    def __init__(self, startPosition, itemManager):
        self.item = itemManager.createAndAddItem(self.BALL_STANDARD_IMAGES,startPosition)
        self.angle = 0
        self.speed = 0  
        self.lastupdate = time.clock()
        self._position = startPosition
   
    
    def shoot(self, carangle, carspeed):
        self.angle = carangle
        self.speed = carspeed
        
    def update(self, ):
        now = time.clock()  
        difference = now - self.lastupdate #einframe
        self._position.x = difference*(self.speed*math.sin(self.angle)) + self._position.x
        self._position.y = difference*(self.speed*math.cos(self.angle)) + self._position.y
        self.lastupdate = now
        self.item.position = self._position
        self.speed = self.speed * (1-0.2*difference)
        
        