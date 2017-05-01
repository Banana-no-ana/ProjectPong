#There are a limited number of event actors on the map. They can be active / nonactive.
class eventActor(object):
    name = "Default placeable"
    description = "Default description"
    actorPriority = NotImplemented
    """ database fields: 
        actor prioritiy : used to figure out if the actor will act in this turn
        actor frequency : used to figure out how often an actor will act
        enabled: if the actor is enabled. If not, then leave it alone. 
    """    

class gameEvent(object):
    name = "Default placeable"
    description = "Default description"
    possibleEffects = []
    activatedEffects = []
    nextEvent = []
    #eventActor = should be one of the actors that are already configured
    #EventRoot = Should be a combo Box. Empty should end up being a top level event
    """ Other fields to consider: 
            event criterias. How would we evaluate these? 
    
        Other considerations:     
            If the event is a top level event, how often should it happen? Everytime the criterias are set?
    """
    
    #Event chance / priority = dictates a priority on this event happening, based on a root event?
    #event Triggers
    

#Something that needs to happen have happened. This may trigger additional events
class gameNotification(object):
    name = "Type of notification"
    description = "What's happening. What's going to happen"
    effects = [] #Fuck if I know what's supposed to be in here lol. 