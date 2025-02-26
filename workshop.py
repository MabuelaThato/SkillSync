import click,datetime,os
from get_user import get_user
from get_users import get_users
from refresh import refresh_creds

def make_workshop(db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return

    user = get_user(db)
    service = refresh_creds()
    if user['role'] != 'mentor':
        click.secho("Only mentors can book workshops", fg= 'red')
        return
    
    options = ['mentors','students','all']

    selected_role = click.prompt(
        "Select who you would like to book a workshop with",
        type=click.Choice(options)
    )

    match selected_role:
        case 'mentors':
            people = get_users('mentor',db)
        case 'students':
            people = get_users('student',db)
        case 'all':
            people = get_users('all',db)

    if user not in people:
        people.append(user)

    date = input('Event date(DD-MM-YYYY): ').strip()
    start_time = input('Event start time (HH-MM): ').strip()
    end_time = input('Event end time (HH-MM): ').strip()

    start_hour = datetime.datetime.strptime(f'{date} {start_time}', "%d-%m-%Y %H:%M")
    end_hour = datetime.datetime.strptime(f'{date} {end_time}', "%d-%m-%Y %H:%M")

    if start_hour.weekday() >= 5 or start_hour.hour < 7 or end_hour.hour > 17:
        click.echo("Invalid time, meetings can only take place on weekdays between 07:00 to 17:00.")
        return
    
    start = start_hour.isoformat() + 'Z'
    end = end_hour.isoformat() + 'Z'
    
    events_result = service.events().list(calendarId='primary', timeMin=start, timeMax = end, singleEvents=True).execute()
    events = events_result.get('items', [])

    if events:
        click.secho('You already have an event for that specified date or time', fg='red')
        return

    title = input("Meeting title: ").strip()
    desc = input("Description of meeting: ").strip()
    location = input("Meeting location: ").strip()

    emails = []

    for person in people:
        emails.append(person['email'])

    event = {'summary': title,
            'description': desc,
             'location' : location,
             'start':{'dateTime': start_hour.isoformat(), 'timeZone': 'UTC+2'},
             'end':{'dateTime': end_hour.isoformat(), 'timeZone': 'UTC+2'},
             'attendees': [{"email": email} for email in emails],
             'reminders': {'useDefault': False,
                            'overrides' : [{'method':'email', 'minutes': 24 * 60},
                                            {'method': 'popup', 'minutes': 15},
                                            ],
                            },
            } 

    created_event = service.events().insert(calendarId='primary', body=event, sendUpdates="all" ).execute()
    click.secho(f"Created event: {created_event['summary']}", fg='green')
