import os, click,pwinput

def login_user(auth, db):
    if os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are already logged in",  fg="green")
    else:
        email = input("Email: ")
        password = pwinput.pwinput()
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            if user:
                try:
                    with open("lib/firebase-creds.txt", "w") as fire_creds:
                        doc_ref = db.collection('users').document(user['localId'])
                        doc = doc_ref.get()
                        fire_creds.write(user['localId'])
                        click.secho("Login successfull", fg='green')
                except FileNotFoundError:
                    click.echo("Failed to login. Please try again.")   
            else:
                click.echo("Failed to login. Please try again.")
        except Exception as e:
            click.echo("You do not have an account or invalid password. Please try again.")
            click.echo("Run 'skill-sync register' to register an account")