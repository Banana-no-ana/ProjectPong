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



#Palceables can be buildings
class PlaceableForm(Form):
    placeableName = StringField('Placeable Name', [validators.Length(min=4, max=20)])
    description = StringField('Describe the intentio nof this placeable', [validators.Length(min=4, max=250)])
    #compatible character classes = undefined
    #compatible upgrade types = undefined

class placeableUpgradeTypeForm(Form):
    typeName = StringField('Type Name', [validators.Length(min=4, max=20)])
    description = StringField('Describe the Intention of this type', [validators.Length(min=4, max=250)])
    
class placeableUpgradeForm(Form):
    typeName = StringField('Type Name', [validators.Length(min=4, max=20)])
    description = StringField('Describe the Intention of this upgrade', [validators.Length(min=4, max=250)])
    #upgradeType = undefined

class CharacterClassForm(Form):
    className = StringField('Character Class Name',[validators.Length(min=4, max=20)])
    classDescription = StringField('Describe the intention of this character class', [validators.Length(min=4, max=250)])
    #classPerks = RollableClass Perks


class EventActorForm(Form):
    actorName = StringField('Event Actor name', [validators.Length(min=4, max=20)])
    description = StringField('Describe the intention of this actor', [validators.Length(min=4, max=250)])


class EventForm(Form):
    eventName = StringField('Event Name', [validators.Length(min=4, max=30)])