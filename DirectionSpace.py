from enum import Enum
class DirectionSpace(Enum):
    UP = (0,1)
    DOWN = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)
    STOP = (0,0)

    DirectionList = ((0,1),(0,-1),(-1,0),(1,0),(0,0))
