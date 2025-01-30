import google.cloud
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def register_user(auth,db):
    click.echo("Please enter your details to register for an account:")
    while True:
        name = input("Fullname: ")
        email = input("Email: ")
        password = pwinput.pwinput()
        if validate_input(email):
            try:
                user = auth.create_user_with_email_and_password(email,password)
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

                    doc_ref = db.collection('users').document(user['localId'])
                    doc_ref.set({u'fullname': name, u'email': email, u'role': "student", u'calendar_id': created_calendar['id']})
                    break

            except Exception as e:
                try:
                    user_email = auth.get_user_by_email(email)
                    if user_email:
                        click.echo("User already exists.")
                        click.echo("Please log in instead.")
                        break
                except:
                    click.echo("Failed to register account. Please try again.")