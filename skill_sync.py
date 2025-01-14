#!/usr/bin/env python3
import os,time,sys
from pyrebase import pyrebase
import click
import pwinput
from dotenv import load_dotenv
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore, auth
# from validate_input import validate_input
# try:
#     from dashboard import dashboard_view
#     print("Import successful")
# except Exception as e:
#     print(f"Import failed: {e}")

load_dotenv()
person = ''

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
store = firestore.client()

users = store.collection("users").stream()
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
                    ctx.obj.user = user["localId"]
                    ctx.obj.db = users
                    break
                else:
                    click.echo("Failed to login. Please try again.")
            except:
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
            print(user["localId"])
            command = input("-> ").strip().lower()
            if command == "logout":
                click.echo("Exiting the program. Goodbye!")
                sys.exit()
            if command in cli.commands:
                ctx.invoke(cli.commands[command])
            else:
                # Display an error message and show the help message
                click.echo(f"Invalid command: {command}")
                click.echo(cli.get_help(ctx))

@click.command()
def register(help="Register an account on SkillSync"):
    click.echo(person)
    click.echo("Please enter your details to register for an account:")
    while True:
        name = input("Fullname: ")
        email = input("Email: ")
        password = pwinput.pwinput()
        if validate_input(password,email):
            try:
                user = authentication.create_user_with_email_and_password(email,password)
                doc_ref = store.collection(u'users')
                doc_ref.add({u'fullname': name, u'email': email, u'role': "student"})
                if user:
                    return user
            except Exception as e:
                try:
                    user_email = auth.get_user_by_email(email)
                    if user_email:
                        click.echo("User already exists.")
                except:
                    click.echo("Failed to register account. Please try again.")

# @click.command()
# @click.pass_context
# @click.option("--person_role", required=True, help="The role of the person you would like to book")
# def book(ctx):
#     while True: 
#         group = input("Would you like to book a meeting with a mentor or student?: ").strip().lower()
#         break

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
# cli.add_command(book)
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
