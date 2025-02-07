import click
from get_events import get_events
from refresh import refresh_creds

def update_event(db):
    user = get_user(db)
    events = get_events(db)
    service = refresh_creds()
    selected_event = click.prompt(
        "Select the event you want to update",
        type=click.Choice(events)
    )

    click.echo("What would you like to update?")
    options = {
        "1": "summary",
        "2": "description",
        "3": "location",
        "4": "start time",
        "5": "end time"
    }

    for key, value in options.items():
        click.echo(f"{key}. {value}")

    choice = input("Enter the number of the field you want to update: ").strip()

    updated_event = selected_event.copy()

    if choice == "1":
        updated_event["summary"] = input("Enter new event title: ").strip()
    elif choice == "2":
        updated_event["description"] = input("Enter new event description: ").strip()
    elif choice == "3":
        updated_event["location"] = input("Enter new event location: ").strip()
    elif choice == "4":
        tz = get_localzone()
        time = input("Enter new start time (YYYY-MM-DD HH:MM): ").strip()
        start_time = tz.localize(datetime.datetime.strptime(time, "%Y-%m-%d %H:%M"))
        updated_event["start"] = {
            "dateTime": start_time.isoformat(),
            "timeZone": str(tz)
        }
    elif choice == "5":
        tz = get_localzone()
        time = input("Enter new end time (YYYY-MM-DD HH:MM): ").strip()
        end_time = tz.localize(datetime.datetime.strptime(time, "%Y-%m-%d %H:%M"))
        updated_event["end"] = {
            "dateTime": end_time.isoformat(),
            "timeZone": str(tz)
        }
    else:
        click.echo("Invalid choice. No changes made.")

    updated_event = service.events().update(
        calendarId=user["calendar_id"],
        eventId=updated_event["id"],
        body=updated_event
    ).execute()

    click.echo(f"Updated event: {updated_event['summary']}")

