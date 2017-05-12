#Describes all the Tile types in the world, As well as tile upgrades


#Start with some outside tiles
class WorldTile(object):
    worldPlaceable = True
    townPlaceable = True

class TownTile (object):
    worldPlaceable = False
    townPlaceable = True

class outsideTile(WorldTile):
    name = 'Supplied'
    description = 'Supplied'
    intendedUsage = 'Unknown'



