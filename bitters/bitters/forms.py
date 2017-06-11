from flask.ext.wtf import Form, BooleanField, StringField, validators, SelectField, TextAreaField, HiddenField, IntegerField
from wtforms import RadioField
from wtforms.fields.html5 import EmailField

class PlayerSignup(Form):
    name = StringField('Name', [validators.Length(min=4, max=30)]) 
    email = StringField('Email for matches', [validators.DataRequired(), validators.Email()], render_kw={"placeholder": "email/calendar for match invitations"})
    avail = SelectField('Max match frequency', choices=[('2', 'Semi-Weekly'),('7', 'Weekly'), ('1', 'Daily'),('14', 'Bi-Weekly'), ('1000', 'Not availabe anymore')])
    coach = SelectField('Are you available for coaching', choices=[('True', 'Yes'), ('False', 'Maybe some other time')])
    del_entity = HiddenField('del_entity')
   
class MatchForm(Form):
    winner = SelectField('Winner of the Match', coerce=unicode)
    loser = SelectField('Seconed place of the match', coerce=unicode)
    win_score = IntegerField('[Optional] Winner score', [validators.Optional()])
    los_score = IntegerField('Loser score',[validators.Optional()])