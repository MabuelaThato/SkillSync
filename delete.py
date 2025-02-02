from get_calendar_service import get_calendar_service
import click
from get_events import get_events

def delete_event(db):
    user = get_user(db)
    events = get_events(db)
    selected_event = click.prompt(
        "Select the event you want to cancel",
        type=click.Choice(events)
    )

    service.events().delete(calendarId=user['calendar_id'], eventId=selected_event['id']).execute()
    click.echo(f"Deleted event: {updated_event['summary']}")