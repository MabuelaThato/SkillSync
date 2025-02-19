import click,os
from get_events import get_events

def view_events(db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return

    events = get_events(db)

    if not events:
        click.echo('No upcoming events found.')
        return
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start.split("T")
        date, time = start[0], start[1].split("+")[0]
        time = time.split(":")
        click.secho(f'{event['summary']}:', fg='blue')
        click.echo(f"Date : {date}")
        click.echo(f"Time : {time[0]}:{time[1]}")