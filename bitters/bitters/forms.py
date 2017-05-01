from flask.ext.wtf import Form, BooleanField, StringField, validators, SelectField
from wtforms import RadioField

class VoteForm(Form):
    deploy_preference  = RadioField('Deployment Preference', choices=[
        ('Web Site', 'Web Site'),
        ('Cloud Service', 'Cloud Service'),
        ('Virtual Machine', 'Virtual Machine')], default='Cloud Service')
    deploy_preference2 = SelectField(u'Deployment Preference', choices=[
        ('Web Site', 'Web Site'),
        ('Cloud Service', 'Cloud Service'),
        ('Virtual Machine', 'Virtual Machine')], default='Cloud Service')


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

#Palceables can be buildings
class Placeables(Form):
    placeableName = StringField('Placeable Name', [validators.Length(min=4, max=20)])
    description = StringField('Describe the intentio nof this placeable', [validators.Length(min=4, max=250)])
    
    """ database fields: 
        position (x,y): Position this thing is placed at. 
        enabled: if this object is enabled
        location: Shoudl be a drop down of in-town or out of town
    """

class CharacterClasses(Form):
    className = StringField('Character Class Name',[validators.Length(min=4, max=20)])
    classDescription = StringField('Describe the intention of this character class', [validators.Length(min=4, max=250)])
    classPlaceable


class EventActors(Form):
    actorName = StringField('Event Actor name', [validators.Length(min=4, max=20)])
    description = StringField('Describe the intention of this actor', [validators.Length(min=4, max=250)])
    """ database fields: 
        actor prioritiy : used to figure out if the actor will act in this turn
        actor frequency : used to figure out how often an actor will act
        enabled: if the actor is enabled. If not, then leave it alone. 
    """
    

class Events(Form):
    eventName = StringField('Event Name', [validators.Length(min=4, max=30)])
    #eventActor = should be one of the actors that are already configured
    #EventRoot = Should be a combo Box. Empty should end up being a top level event
    """ Other fields to consider: 
            event criterias. How would we evaluate these? 
    
        Other considerations:     
            If the event is a top level event, how often should it happen? Everytime the criterias are set?
    """

    
    #Event chance / priority = dictates a priority on this event happening, based on a root event?
    #event Triggers
    