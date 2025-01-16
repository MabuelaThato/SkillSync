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
bookings = db.collection("bookings")

class CustomContext:
    def __init__(self):
        self.user = None
        self.data = {}

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Welcome to Skill Sync!")
        time.sleep(1)
        click.echo("Please enter your details to login: ")
        ctx.ensure_object(CustomContext)
        # for user in users:
        #     print(user.to_dict())
        while True:
            time.sleep(1)
            email = input("Email: ")
            password = pwinput.pwinput()
            try:
                user = authentication.sign_in_with_email_and_password(email, password)
                if user:
                    ctx.obj.bookings = bookings.stream()
                    mentors = []
                    students = []

                    for person in users.stream():
                        if user["localId"].strip() == person.to_dict()["user_id"]:
                            ctx.obj.user = person.to_dict()
                        elif person.to_dict()["role"] == "mentor":
                            mentors.append(person)
                        else:
                            students.append(person)

                    ctx.obj.mentors = mentors
                    ctx.obj.students = students
                    break
                else:
                    click.echo("Failed to login. Please try again.")
            except Exception as e:
                click.echo(e)
                try:
                    user_email = auth.get_user_by_email(email)
                    if user_email:
                        click.echo("Invalid password. Please try again.")
                except:
                    click.echo("You do not have an account...")
                    user = register()
                    ctx.obj.user = user["localId"]
                    ctx.obj.db = users
                    break

        while True:
            print(ctx.obj.user)
            command = input("Enter command -> ").strip().lower()
            if command == "logout":
                click.secho("Exiting the program. Goodbye!",fg="blue")
                sys.exit()
            if command in cli.commands:
                ctx.invoke(cli.commands[command])
            else:
                # Display an error message and show the help message
                click.echo(f"Invalid command: {command}")
                click.echo(cli.get_help(ctx))

@click.command()
@click.pass_context
def register(ctx, help="Register an account on SkillSync"):
    click.echo(ctx.obj.user)
    click.echo("Please enter your details to register for an account:")
    while True:
        name = input("Fullname: ")
        email = input("Email: ")
        password = pwinput.pwinput()
        if validate_input(password,email):
            try:
                user = authentication.create_user_with_email_and_password(email,password)
                doc_ref = db.collection(u'users')
                doc_ref.add({u'fullname': name, u'email': email, u'role': "student", u'user_id' : user["localId"]})
                if user:
                    return user
            except Exception as e:
                try:
                    user_email = auth.get_user_by_email(email)
                    if user_email:
                        click.echo("User already exists.")
                except:
                    click.echo("Failed to register account. Please try again.")

@click.command()
@click.pass_context
def book(ctx):
    while True:
        role = click.prompt("Would you like to book a mentor or a student? ").strip().lower()
        if role == "mentor":
            people = ctx.obj.mentors
            break
        elif role == "student":
            people = ctx.obj.students
            break
        else:
            click.echo("Please enter 'mentor' or 'student'")

    people_dict = {}
    for person in people:
        person_dict = person.to_dict()
        click.echo(f"-> {person_dict["fullname"]}")
        people_dict[person_dict["fullname"]] = f'{person_dict["email"]}, {person.id}'
 
    while True:
        name = click.prompt("Enter the fullname of the person you would like to book").strip()
        if name in list(people_dict.keys()):
            break
        else:
            click.echo("Please enter a name from the list. E.g. Thato Mabuela")

    email, user_doc_id = people_dict[name].split(",")

    date = click.prompt("Enter a date for the meeting")
    time = click.prompt("Enter a time for the meeting")

    current_user = ctx.obj.user
    user_name = current_user["fullname"]
    user_email = current_user["email"]
    user_id = current_user["user_id"]


    bookings.add({u'date': date, u'time': time, u'person1': f"{name},{email},{user_doc_id}", u'person2': f"{user_name},{user_email},{user_id}"})
    click.secho(f"Meeting booked successfully",fg="green")
        

@click.command()
@click.pass_context
def test(ctx):
    try:
        while True:
            print(ctx.obj.user["localId"])
            command = input("-> ").strip().lower()
            if command == "logout":
                click.echo("Exiting the program. Goodbye!")
                sys.exit()
            ctx.invoke(cli.commands.get(command))
    except Exception as e:
        sys.exit("Invalid command")

cli.add_command(register)
cli.add_command(book)
cli.add_command(test)

def validate_input(password, email):
    password_length = len(password)
    password_chars = list(password)

    digits = 0
    uppercases = 0
    lowercases = 0
    special_chars = 0

    for char in password_chars:
        if char.isalnum():
            if char.isdigit():
                digits += 1
            elif char.isupper():
                uppercases += 1
            elif char.islower():
                lowercases += 1
        else:
            if char != " ":
                special_chars += 1

    if digits > 0 and uppercases > 0 and lowercases > 0 and special_chars > 0 and password_length >= 8:
        if "@student.wethinkcode.co.za" in email:
            return True
    
    return False   

if __name__ == "__main__":
    cli()
