import click
def logout_user():
    if os.path('lib/firebase-creds.txt'):
        os.remove('lib/firebase-creds.txt')
        click.secho("You have successfully been logged out", fg='green')
    else:
        click.echo("You are not logged in.")