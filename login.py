import os, click,pwinput
from rich.console import Console

def login_user(auth):
    if os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are already logged in",  fg="green")
    else:
        console = Console(width=70)
        email = input("Email: ")
        password = pwinput.pwinput()
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            if user:
                try:
                    with open("lib/firebase-creds.txt", "w") as fire_creds:
                        fire_creds.write(user['localId'])
                        click.clear()
                        click.echo("")
                        console.print("Welcome to SkillSync", style="bold white on green", justify='center')
                        click.echo("")
                        click.echo("You have been logged in successfully")
                        click.echo("Run 'python skill-sync --help' to get a list of the commands available")
                        click.echo("")
                except FileNotFoundError:
                    click.echo("Failed to login. Please try again.")   
            else:
                click.echo("Failed to login. Please try again.")
        except Exception as e:
            click.secho("You do not have an account or invalid password. Please try again.", fg='red')
            click.echo("Run 'skill-sync register' to register an account")