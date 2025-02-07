import click
from get_previous_events import get_previous
from refresh import refresh_creds
from send_email import send_email

def feedback(db):
    user = get_user(db)
    events = get_previous(db)
    selected_event = click.prompt(
        "Select the event you want to give feedback on",
        type=click.Choice(events)
    )
    emails = selected_event['emails'].split(',')
    title = input("Enter title for feedback:\n")
    message  = input('Enter feedback:\n')
    send_email(emails[0],emails[1],user['calendar_id'],message,title)