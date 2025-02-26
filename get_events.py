import click, os, datetime
from refresh import refresh_creds

def get_events():
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
    
    service = refresh_creds()

    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        return events
    except Exception as e:
        click.secho(f"Error retrieving events: {e}", fg='red')
        return None