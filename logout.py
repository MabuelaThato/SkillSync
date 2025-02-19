import click,os
def logout_user():
    if os.path.exists('lib/firebase-creds.txt'):
        os.remove('lib/firebase-creds.txt')
        click.secho("You have successfully been logged out", fg='green')
    else:
        click.echo("You are not logged in.")