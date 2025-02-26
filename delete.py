import click,os
from get_events import get_events
from refresh import refresh_creds
from get_user import get_user

def delete_event(db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
        
    user = get_user(db)
    events = get_events(db)
    service = refresh_creds()

    count = 0
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start.split("T")
        date, time = start[0], start[1].split("+")[0]
        time = time.split(":")
        click.secho(f'{count}.{event['summary']}:', fg='blue')
        click.echo(f"Date : {date}")
        click.echo(f"Time : {time[0]}:{time[1]}")
        count += 1
        
    try:
        choice = int(input("Enter the number of the event you would like to cancel: ").strip())
    except ValueError:
        click.secho(f"Invalid input. Enter a number (from 0 to {len(events)})", fg='red')
        return
    
    selected_event = list(events)[choice]

    deleted_event = service.events().delete(calendarId='primary', eventId=selected_event['id'], sendUpdates="all").execute()
    click.secho(f"Event deleted successfully", fg='green')