import click
from get_calendar_service import get_calendar_service

def get_events(db):
    if not os.path('lib/firebase-creds.txt'):
        click.echo("You are not logged in")
        return
        
    user = get_user(db)
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat()
    click.echo('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=user['calendar_id'], timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events