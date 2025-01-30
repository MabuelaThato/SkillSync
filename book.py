from refresh import refresh_creds

def make_booking():
    service = refresh()

    person_role = input("Enter role of person you would like to book")
    desc = input("Description of meeting: ").strip()
    location = input("Meeting location: ").strip()
    num = input("Number of attendees(eg. 1 or 6): ")
    click.echo("Enter emails of attendees:")
    emails = []
    for i in range(int(num)):
        email = input(f"{i + 1}: ").strip()
        emails.append(email)

    while True:
        s_time = input("Start time (format: 14-05): ").strip()
        e_time = input("End time (format: 17-05): ").strip()
        day = input("Date of meeting (dd/mm/yy): ").strip()

        start = datetime.datetime.strptime(f"{day} {s_time}", "%d-%m-%Y %H:%M")
        end = datetime.datetime.strptime(f"{day} {e_time}", "%d-%m-%Y %H:%M")

        if start.weekday() >=5 or start.hour() < 7 or end.hour() >= 17:
            click.secho("You can only book meetings for weekdays between 07:00 and 17:00.", fg = 'red')
            click.echo("Please try again.")
        
        else:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=start.isoformat() + 'Z', timeMax = end.isoformat() + 'Z', singleEvents=True).execute()
            events = events_result.get('items', [])

            if events:
                click.secho('You already have an event for that specified date or time', fg='red')
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    click.echo(start, event['summary'])
            else:
                event = {
                    'summary': 'One on one meeting',
                    'location': location,
                    'description': desc,
                    'start': {
                        'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat(),
                        'timeZone': 'Africa/Johannesburg',
                    },
                    'end': {
                        'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
                        'timeZone': 'Africa/Johannesburg',
                    },
                }
                userid, calendarid = get_info()
                created_event = service.events().insert(calendarId=calendarid, body=event).execute()
                click.echo(f"Created event: {created_event['id']}")
                doc_ref = db.collection('bookings')