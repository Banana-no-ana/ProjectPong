#Entity configurations. 
from gameEvents import eventActor
from character import characterClass

"""
Event driving philosophy: 
Objets on the map are placeables. 
Placeable items can have associated characters with them. For example, the blacksmith class can be placed into the blacksmith placeable. 
    Maybe the merchant class can be placed into the blacksmith placeable as well. 
Placeable items may have upgrades. 
    Example: blacksmith character expansion. Blackmisth shop expansion. Blacksmith finance expansion. 
Almost all placeables will have events. Events are listed first from the Placeable itself, then from the characters, then character perks. 


- Resource production is not an event, but can be affected by events. Resource production is calculated at the end of the turn. 
- Placeables may also have resource demands, production, as well as consumption. All 3 are calculated from placeable attributes, character attributes, then perks. 


"""

class placeableUpgradeType(object):
    def __init__(self):
        name = "Default placeable"
        description = "Default description"

class placeableUpgrade(object):
    name = "Default upgrade"
    description = "Default description"
    upgradeType = placeableUpgradeType()    

#Palceables can be buildings
class placeableType(object):
    def __init__(self):
        self.id = "Default ID"
        self.name = "Default placeable"
        self.description = "Default description"
        self.allowedUpgrades = [] #placeableUpgradeType()
        self.allowedCharacterClasses = [] #characterClass()
        #isEventActor = True #Default all placeables are events
        self.currentEventActor = None  #Default eventActor
    #TileType = Undefined as of yet
    

    """ database fields: 
        position (x,y): Position this thing is placed at. 
        enabled: if this object is enabled
        event categories / event list
        character categories / character list
        upgrade categories / upgrade list
        event priority / event frequency
    """

