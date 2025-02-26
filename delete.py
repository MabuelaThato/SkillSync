import click,os
from get_events import get_events
from refresh import refresh_creds
from rich.console import Console
from rich.table import Table

def delete_event():
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
        
    events = get_events()
    service = refresh_creds()
    console = Console()

    table = Table(title="Upcoming events (max 5)")
    table.add_column("No.", justify="center")
    table.add_column("Title", justify="center")
    table.add_column("Date", justify="center")
    table.add_column("Time", justify="center")
    count = 0
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start.split("T")
        date, time = start[0], start[1].split("+")[0]
        time = time.split(":")
        table.add_row(f'{count}',f'{event['summary']}', f"{date}", f"{int(time[0]) + 2}:{time[1]}")
        count += 1

    console.print(table)
        
    try:
        choice = int(input("Enter the number of the event you would like to cancel: ").strip())
    except ValueError:
        click.secho(f"Invalid input. Enter a number (from 0 to {len(events)})", fg='red')
        return
    
    selected_event = list(events)[choice]

    deleted_event = service.events().delete(calendarId='primary', eventId=selected_event['id'], sendUpdates="all").execute()
    click.secho(f"Event deleted successfully", fg='green')