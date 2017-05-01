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


class Events(Form):
    eventName = StringField('Event Name', [validators.Length(min=4, max=30)])
    #EventRoot = Should be a combo Box. Empty should end up being a top level event
    #eventClass = should dictate what kind of event this is.
    #Event chance / priority = dictates a priority on this event happening, based on a root event?
    #event Triggers
    