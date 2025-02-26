import click, os
from get_previous_events import get_previous
from send_email import send_email
from get_user import get_user
from rich.console import Console
from rich.table import Table

def feedback(db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
        
    user = get_user(db)
    events = get_previous()
    console = Console()

    table = Table(title="Previous events (max 5)")
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
        choice = int(input("Enter the number of the event you would like to give feedback on: ").strip())
    except ValueError:
        click.secho(f"Invalid input. Enter a number (from 0 to {len(events)})", fg='red')
        return
    
    selected_event = list(events)[choice]

    attendees = selected_event['attendees']
    title = f'{selected_event['summary']} - feedback'
    message  = input('Enter feedback:\n')

    try:
        click.echo("Sending feedback...")
        for person in attendees:
            send_email(user['email'],person['email'],"lmquuljszksvixto",message,title)

        click.secho("Feedback sent successfully", fg='green')
    except:
        click.secho("Failed to send feedback. Please try again", fg='red')
    