#!/usr/bin/env python3
import os,time,sys
from pyrebase import pyrebase
import click, pwinput
from dotenv import load_dotenv
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore, auth
from login import login_user
from logout import logout_user
from register import register_user

load_dotenv()

config = {
    "apiKey": os.environ.get("API_KEY"),
    "authDomain": os.environ.get("AUTH_DOMAIN"),
    "projectId": os.environ.get("PROJECT_ID"),
    "storageBucket": os.environ.get("STORAGE_BUCKET"),
    "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
    "appId": os.environ.get("APP_ID"),
    "measurementId": os.environ.get("MEASUREMENT_ID"),
    "databaseURL": "",
}

firebase = pyrebase.initialize_app(config)
authentication = firebase.auth()
cred = credentials.Certificate("skillsync-firebase-adminsdk.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

@click.group()
def cli():
    pass

@click.command()
def login(help="Log into SkillSync"):
    login_user(authentication,db)

@click.command()
def register(help="Register an account on SkillSync"):
    register_user(authentication, db)

@click.command()
def book():
    person_role = input("Enter role of person you would like to book")
    desc = input("Description of meeting: ").strip()
    location = input("Meeting location: ").strip()
    num = input("Number of attendees(eg. 1 or 6): ")
    click.echo("Enter emails of attendees:")
    emails = []
    for i in range(int(num)):
        email = input(f"{i + 1}: ").strip()
        emails.append(email)

    while True:
        s_time = input("Start time (format: 14-05): ").strip()
        e_time = input("End time (format: 17-05): ").strip()
        day = input("Date of meeting (dd/mm/yy): ").strip()

        start = datetime.datetime.strptime(f"{day} {s_time}", "%d-%m-%Y %H:%M")
        end = datetime.datetime.strptime(f"{day} {e_time}", "%d-%m-%Y %H:%M")

        if start.weekday() >=5 or start.hour() < 7 or end.hour() >= 17:
            click.secho("You can only book meetings for weekdays between 07:00 and 17:00.", fg = 'red')
            click.echo("Please try again.")
        
        else:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=start.isoformat() + 'Z', timeMax = end.isoformat() + 'Z', singleEvents=True).execute()
            events = events_result.get('items', [])

            if events:
                click.secho('You already have an event for that specified date or time', fg='red')
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    click.echo(start, event['summary'])
            else:
                event = {
                    'summary': 'One on one meeting',
                    'location': location,
                    'description': desc,
                    'start': {
                        'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat(),
                        'timeZone': 'Africa/Johannesburg',
                    },
                    'end': {
                        'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
                        'timeZone': 'Africa/Johannesburg',
                    },
                }
                userid, calendarid = get_info()
                created_event = service.events().insert(calendarId=calendarid, body=event).execute()
                click.echo(f"Created event: {created_event['id']}")
                doc_ref = db.collection('bookings')
        

@click.command()
def view():


@click.command()
def logout(help="Log out of Skill-sync"):
    logout_user()

cli.add_command(register)
cli.add_command(login)
cli.add_command(logout)
cli.add_command(book)
cli.add_command(view)

def validate_input(password, email):
    if "@student.wethinkcode.co.za" in email:
        return True
    
    return False   

if __name__ == "__main__":
    cli()
