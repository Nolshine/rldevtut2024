import constants.colors as colors
from components.components import Graphic

player = {
    "Name": "Player",
    "Graphic": Graphic("@", colors.WHITE), 
    "IsBlocking": True,
}

orc = {
    "Name": "orc",
    "Graphic": Graphic("o", colors.ORC), 
    "IsBlocking": True,
}

troll = {
    "Name": "Player",
    "Graphic": Graphic("T", colors.TROLL), 
    "IsBlocking": True,
}
