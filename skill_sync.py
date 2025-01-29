#!/usr/bin/env python3
import os,time,sys
from pyrebase import pyrebase
import click, pwinput
from dotenv import load_dotenv
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore, auth

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

users = db.collection('users')

def refresh_creds():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        return None

    if  not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    
    return creds
        

@click.group()
def cli():
    pass

@click.command()
def login(help="Log into SkillSync"):
    if os.path('lib/firebase-creds.txt'):
        click.echo("You are already logged in")
    else:
        while True:
            email = input("Email: ")
            password = pwinput.pwinput()
            try:
                user = authentication.sign_in_with_email_and_password(email, password)
                if user:
                    try:
                        with open("lib/firebase-creds.txt", "w") as fire_creds:
                            fire_creds.write(user['localId'])
                        break
                    except FileNotFoundError:
                        click.echo("Failed to login. Please try again.")   
                else:
                    click.echo("Failed to login. Please try again.")
            except Exception as e:
                try:
                    user_email = auth.get_user_by_email(email)
                    if user_email:
                        click.echo("Invalid password. Please try again.")
                except:
                    click.echo("You do not have an account...")
                    click.echo("Run 'skill-sync register' to create an account")
                    break

@click.command()
def register(help="Register an account on SkillSync"):
    click.echo("Please enter your details to register for an account:")
    while True:
        name = input("Fullname: ")
        email = input("Email: ")
        password = pwinput.pwinput()
        if validate_input(email):
            try:
                user = authentication.create_user_with_email_and_password(email,password)
                flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

                service = build('calendar', 'v3', credentials=creds)
                new_calendar = {
                    'summary': 'Skill-sync Calendar',
                }
                created_calendar = service.calendars().insert(body=new_calendar).execute()
                if user:
                    with open('lib/firebase-creds.txt', 'w') as fire_creds:
                        fire_creds.write(user['localId'])
                    doc_ref = db.collection(u'users')
                    doc_ref.add({u'fullname': name, u'email': email, u'role': "student", u'user_id' : user["localId"]}, u'calendar_id': created_calendar['id'])

            except Exception as e:
                try:
                    user_email = auth.get_user_by_email(email)
                    if user_email:
                        click.echo("User already exists.")
                except:
                    click.echo("Failed to register account. Please try again.")

@click.command()
def book():
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
        
        # else:
        #     event = {
        #         'summary': 'Python Meeting',
        #         'location': '800 Howard St., San Francisco, CA 94103',
        #         'description': 'A meeting to discuss Python projects.',
        #         'start': {
        #             'dateTime': start.isoformat() ,
        #             'timeZone': 'America/Los_Angeles',
        #         },
        #         'end': {
        #             'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
        #             'timeZone': 'America/Los_Angeles',
        #         },
        #     }
        #     created_event = service.events().insert(calendarId=created_calendar['id'], body=event).execute()
        #     print(f"Created event: {created_event['id']}")


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
    created_event = service.events().insert(calendarId=created_calendar['id'], body=event).execute()
    print(f"Created event: {created_event['id']}")
        

@click.command()
def view():


@click.command()
def logout(help="Log out of Skill-sync"):
    if os.path('lib/firebase-creds.txt'):
        os.remove('lib/firebase-creds.txt')
    else:
        click.echo("You are not logged in.")

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
