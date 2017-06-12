import sendgrid
import os
from sendgrid.helpers.mail import *
import config

import pytz
import datetime as dt
import icalendar
import base64

import uuid
from icalendar import Calendar, Event

 
def makeiCal2(subj, description):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', 'Python meeting about calendaring')
    try:
        event.add('dtstart', dt.datetime(2017,7,7,8,0,0,tzinfo=pytz.utc))
        event.add('dtend', dt.datetime(2017,7,7,10,0,0,tzinfo=pytz.utc))
        event.add('dtstamp', dt.datetime(2017,7,7,0,10,0,tzinfo=pytz.utc))
    except Exception as e:
        pass
    
    from icalendar import vCalAddress, vText
    organizer = vCalAddress('MAILTO:devcenterpingpong@outlook.com')

    organizer.params['cn'] = vText('Dan Piao')
    organizer.params['role'] = vText('CHAIR')
    event['organizer'] = organizer
    event['location'] = vText('Online')

    event['uid'] = '20050115T101010/27346262376@mxm.dk'
    event.add('priority', 5)

    attendee = vCalAddress('MAILTO:bpdaniel@outlook.com')
    attendee.params['cn'] = vText('Outlook')
    attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
    event.add('attendee', attendee, encode=0)

    attendee = vCalAddress('MAILTO:dimshadow101@gmail.com')
    attendee.params['cn'] = vText('Other Dan')
    attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
    event.add('attendee', attendee, encode=0)

    cal.add_component(event)
    return cal.to_ical()


def sendemail():
    sg = sendgrid.SendGridAPIClient(apikey=config.SENDGRID_API_KEY)
    from_email = Email("devcenterpingpong@outlook.com")
    to_email = Email("bpdaniel@outlook.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)

    #ical = makeiCal("Let's make a calendar", "Calendars are super cool")
    ical = makeiCal2("Nothing", "Nomore")
    ical64 = base64.standard_b64encode(ical)
    attachment = Attachment()
    attachment.content = ical64
    attachment.type = 'text/calendar'
    attachment.filename = 'invite.ics'
    attachment.content_id = uuid.uuid4().hex

    mail.add_attachment(attachment)
    
    #response = sg.client.mail.send.post(request_body=mail.get())

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except Exception as e:
        print(e)

    #except urllib.HTTPError as e:
        #print(e.read())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def mailHelper(object):
    def __init__(self):
        self.date = dt.datetime.now()
        pass