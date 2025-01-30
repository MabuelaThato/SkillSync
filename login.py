import os, click

def login_user(auth, db):
    if os.path('lib/firebase-creds.txt'):
        click.echo("You are already logged in")
    else:
        while True:
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
                            fire_creds.write(doc['calender_id'])
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