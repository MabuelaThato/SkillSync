import os,time,sys
from pyrebase import pyrebase
import click, pwinput
from dotenv import load_dotenv
import google.cloud
from firebase_admin import credentials, firestore, auth, firebase_admin
from login import login_user
from logout import logout_user
from register import register_user
from book import make_booking
from view import view_events
from delete import delete_event
from update import update_event
from workshop import make_workshop
from feedback import feedback


load_dotenv()

config = {
    "apiKey": os.environ.get("API_KEY"),
    "authDomain": os.environ.get("AUTH_DOMAIN"),
    "projectId": os.environ.get("PROJECT_ID"),
    "storageBucket": os.environ.get("STORAGE_BUCKET"),
    "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
    "appId": os.environ.get("APP_ID"),
    "measurementId": os.environ.get("MEASUREMENT_ID"),
    "databaseURL": os.environ.get("DATABASE_URL"),
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
def book_meeting(help="Book one on one meetings"):
    make_booking(db)

@click.command()
def book_workshop(help="Book all mentors/student/both"):
    make_workshop(db)     

@click.command()
def view(help="view your upcoming events"):
    view_events(db)

@click.command()
def update(help="Update an event"):
    update_event(db)

@click.command()
def cancel(help="Cancel an event"):
    delete_event(db)

@click.command()
def give_feedback(help="Send feedback to attendees"):
    feedback(db)


@click.command()
def logout(help="Log out of SkillSync"):
    logout_user()

cli.add_command(register)
cli.add_command(login)
cli.add_command(logout)
cli.add_command(book_meeting)
cli.add_command(book_workshop)
cli.add_command(view)
cli.add_command(update)
cli.add_command(cancel)
cli.add_command(give_feedback)

def validate_input(email):
    if "@student.wethinkcode.co.za" in email:
        return True
    
    return False   

if __name__ == "__main__":
    cli()
