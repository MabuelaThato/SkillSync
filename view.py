import click
from get_events import get_events

def view_events(db):

    events = get_events(db)

    if not events:
        click.secho('No upcoming events found.', fg='orange')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        click.echo(start, event['summary'])