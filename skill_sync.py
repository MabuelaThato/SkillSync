#!/usr/bin/env python3
import os,time,sys
from pyrebase import pyrebase
import click
import pwinput
from dotenv import load_dotenv

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
auth = firebase.auth()

@click.group()
def cli():
    pass

@click.command()
def run():
    click.echo("Welcome to Skill Sync!")
    time.sleep(1)
    click.echo("Please enter your details to login: ")
    time.sleep(1)
    email = input("Email: ")
    password = pwinput.pwinput()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        if user:
            dashboard(user["idToken"])
        else:
            click.echo("Try registering first")
    except Exception as e:
        click.echo("You do not have an account...")
        register()

def register():
    click.echo("Please enter your details to register for an account:")
    #name = input("Fullname: ")
    email = input("Email: ")
    password = pwinput.pwinput()
    if validate_input(password,email):
        try:
            user = auth.create_user_with_email_and_password(email,password)
            if user:
                dashboard(user["idToken"])
        except Exception as e:
            click.echo(e)

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
        
def dashboard(user):
    click.echo(user)

def logout(user):
    sys.exit()

cli.add_command(run)
