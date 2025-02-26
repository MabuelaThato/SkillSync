import click,os
from get_events import get_events
from rich.console import Console
from rich.table import Table

def view_events():
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return

    console = Console()
    events = get_events()
    table = Table(title="Upcoming events (max 5)")
    table.add_column("No.", justify="center")
    table.add_column("Title", justify="center")
    table.add_column("Date", justify="center")
    table.add_column("Time", justify="center")

    if not events:
        click.echo('No upcoming events found.')
        return
    count = 0
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start.split("T")
        date, time = start[0], start[1].split("+")[0]
        time = time.split(":")
        table.add_row(f'{count}',f'{event['summary']}', f"{date}", f"{int(time[0]) + 2}:{time[1]}")
        count += 1

    console.print(table)