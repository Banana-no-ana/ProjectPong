class characterClass(object):
    name = "Default placeable"
    description = "Default description"
    allowedPerks = [characterPerk()]

class character(object):
    name = "default char"
    description = "Default description"
    charClass = characterClass()

class characterPerk(object):
    name = "default char perk"
    description = "Default description"
    characterSpecific = NotImplemented #Some perks are specific to certain characters
    perkNext = NotImplemented #intended for perk trees and upgradeable perks
