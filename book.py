from refresh import refresh_creds
import click, datetime,os
from get_users import get_users
from get_user import get_user

def make_booking(db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return

    service = refresh_creds()
    person_role = click.prompt(
        "Select role of person you would like to book",
        type=click.Choice(['mentor','student'])
    )

    users = get_users(person_role,db)
    current_user = get_user(db)

    date = input('Event date(DD-MM-YYYY): ').strip()
    start_time = input('Event start time (HH-MM): ').strip()
    end_time = input('Event end time (HH-MM): ').strip()

    start_hour = datetime.datetime.strptime(f'{date} {start_time}', "%d-%m-%Y %H:%M")
    end_hour = datetime.datetime.strptime(f'{date} {end_time}', "%d-%m-%Y %H:%M")

    if start_hour.weekday() >= 5 or start_hour.hour < 7 or end_hour.hour > 17:
        click.echo("Invalid time, meetings can only take place on weekdays between 07:00 to 17:00.")
        return
    
    time_min = start_hour.isoformat() + 'Z'
    time_max = end_hour.isoformat() + 'Z'

    event_result = service.events().list( calendarId='primary', timeMin=time_min, timeMax=time_max, singleEvents=True).execute()
    events = event_result.get('items', [])

    if events:
        click.secho('You already have an event for that specified date or time', fg='red')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            click.echo(start, event['summary'])
        return
    
    available_users = {}

    for user in users:
        available_users[user['fullname']] = user
    
    selected_user = click.prompt(
        "Select a user",
        type=click.Choice(list(available_users.keys()))
    )

    title = input("Meeting title: ").strip()
    desc = input("Description of meeting: ").strip()
    location = input("Meeting location: ").strip()
    attendees = [current_user['email'], available_users[selected_user]['email']]
    
    event = {'summary': title,
            'description': desc,
             'location' : location,
             'start':{'dateTime': start_hour.isoformat(), 'timeZone': 'UTC+2'},
             'end':{'dateTime': end_hour.isoformat(), 'timeZone': 'UTC+2'},
             'attendees': [{'email': email.strip() for email in attendees}],
             'reminders': {'useDefault': False,
                            'overrides' : [{'method':'email', 'minutes': 24 * 60},
                                            {'method': 'popup', 'minutes': 15},
                                            ],
                            },
            }    
    try:
        created_event = service.events().insert(calendarId='primary', body=event,sendUpdates='all').execute()
        doc_ref = db.collection('bookings').document(created_event['id'])
        doc_ref.set({u'emails' : f"{current_user['email']},{available_users[selected_user]['email']}", u'organiser' : current_user['id'], u'attendee': available_users[selected_user]['id'], u'date' : date, u'time' : start_time})
        click.secho(f"Created event: {created_event['summary']}", fg='green')
    except Exception as e:
        click.secho(f'An error occured: {e}', fg='red')
    