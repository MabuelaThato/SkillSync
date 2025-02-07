from refresh import refresh_creds
import click
from get_users import get_users
from get_user import gt_user
from tzlocal import get_localzone

def is_user_available(calendar_id, start_time, end_time):
    service = refresh_creds()
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    return len(events) == 0

def make_booking(db):
    service = refresh_creds()
    person_role = input("Enter role of person you would like to book (mentor or student): ").strip().lower()
    if person_role not in ['mentor','student']
        click.echo("Invalid role entered.")
        return

    users = get_users(person_role)

    s_time = input("Start time (format: YYYY-MM-DD HH:MM): ").strip()
    e_time = input("End time (format: YYYY-MM-DD HH:MM): ").strip()

    tz = get_localzone()
    start_time = tz.localize(datetime.datetime.strptime(s_time, "%Y-%m-%d %H:%M"))
    end_time = tz.localize(datetime.datetime.strptime(e_time, "%Y-%m-%d %H:%M"))

    if start_time.weekday() >=5 or start_time.hour() < 7 or end_time.hour() >= 17:
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

    available_users = {}

    for user in users:
        if is_user_available(user['calendar_id'], start_time, end_time):
            available_users[user['fullname']] = user
    
    if not available_users:
        click.echo("No users are available for this time slot.")
        return
    
    selected_user = click.prompt(
        "Select a user",
        type=click.Choice(list(available_users.keys()))
    )

    title = input("Meeting title: ").strip()
    desc = input("Description of meeting: ").strip()
    location = input("Meeting location: ").strip()

    user = get_user(db)

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
            {"email": user['email']}, 
            {"email": available_users[selected_user]['email']},
        ],
        }
    created_event = service.events().insert(calendarId=user['calender_id'], body=event).execute()
    doc_ref = db.collection('bookings').document(created_event['id'])
    doc_ref.set({u'emails' : f"{user['email']},{available_users[selected_user]['email']}", u'organiser' : user.id, u'attendees': available_users[selected_user].id, u'date' : start_time})
    click.echo(f"Created event: {created_event['id']}")