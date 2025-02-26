import click,os, datetime
from get_events import get_events
from refresh import refresh_creds

def update_event(db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
        
    events = get_events(db)

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
        choice = int(input("Enter the number of the event you would like to update:").strip())
    except ValueError:
        click.echo(f"Invalid input. Enter a number (from 0 to {len(events)})")
        return

    selected_event = list(events)[choice]

    service = refresh_creds()

    date = input('Event date(DD-MM-YYYY): ').strip()
    start_time = input('Event start time (HH-MM): ').strip()
    end_time = input('Event end time (HH-MM): ').strip()
    start_hour = datetime.datetime.strptime(f'{date} {start_time}', "%d-%m-%Y %H:%M")
    end_hour = datetime.datetime.strptime(f'{date} {end_time}', "%d-%m-%Y %H:%M")

    if start_hour.weekday() >= 5 or start_hour.hour < 7 or end_hour.hour > 17:
        click.echo("Invalid time, meetings can only take place on weekdays between 07:00 to 17:00.")
        return
    
    selected_event["start"] = {
            'dateTime': start_hour.isoformat(),
            'timeZone': 'UTC+2'
        }
    selected_event["end"] = {
        'dateTime': end_hour.isoformat(),
        'timeZone': 'UTC+2'
    }


    updated_event = service.events().update(
        calendarId="primary",
        eventId=selected_event["id"],
        body=selected_event,
        sendUpdates="all" 
    ).execute()

    click.secho(f"Updated event: {updated_event['summary']}", fg='green')

