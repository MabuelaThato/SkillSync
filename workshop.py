import click
from get_user import get_user
from get_users import get_users

def make_workshop(db):
    user = get_user(db)
    if user['role'] != 'mentor':
        click.secho("Only mentors can book workshops", fg= 'red')
        return
    
    options = ['mentors','student','all']

    selected_role = click.prompt(
        "Select who you would like to book a workshop with",
        type=click.Choice(options)
    )

    match selected_role:
        case 'mentors':
            people = get_users('mentor')
        case 'students':
            people = get_users('student')
        case 'all':
            mentors = get_users('mentor')
            students = get_users('students')
            people = mentors + students

    if user not in people:
        people.append(person)
    

    s_time = input("Start time (format: YYYY-MM-DD HH:MM): ").strip()
    e_time = input("End time (format: YYYY-MM-DD HH:MM): ").strip()

    tz = get_localzone()
    start_time = tz.localize(datetime.datetime.strptime(s_time, "%Y-%m-%d %H:%M"))
    end_time = tz.localize(datetime.datetime.strptime(e_time, "%Y-%m-%d %H:%M"))

    if start_time.weekday() >= 5 or start_time.hour() < 7 or end_time.hour() >= 17:
        click.secho("You can only book meetings for weekdays between 07:00 and 17:00.", fg = 'red')
        click.echo("Please try again.")
        return
    
    events_result = service.events().list(calendarId='primary', timeMin=start.isoformat(), timeMax = end.isoformat(), singleEvents=True).execute()
    events = events_result.get('items', [])

    if events:
        click.secho('You already have an event for that specified date or time', fg='red')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            click.echo(start, event['summary'])
        return

     title = input("Meeting title: ").strip()
    desc = input("Description of meeting: ").strip()
    location = input("Meeting location: ").strip()

    emails = []

    for person in people:
        emails.append(person['email'])

    event = {
        'summary': title,
        'location': location,
        'description': desc,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': str(tz),
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': str(tz),
        },
        "attendees": [
            {"email": person['email']} for person in people
        ],
        }
    created_event = service.events().insert(calendarId=user['calender_id'], body=event).execute()
    doc_ref = db.collection('bookings').document(created_event['id'])
    doc_ref.set({u'emails' : f"{[person['email'] for person in person]}", u'organiser' : user.id, u'attendees': f"{[person.id for person in person]}", u'date' : start_time})
    click.echo(f"Created event: {created_event['id']}")
