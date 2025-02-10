from refresh import refresh_creds
import datetime

def get_previous(db):
    if not os.path('lib/firebase-creds.txt'):
        click.echo("You are not logged in")
        return

    docs = db.collection('bookings').where('date', '<', datetime.datetime.now()).stream()  # check correctness

    users_dicts = []

    for doc in docs:
        users_dicts.append(doc.to_dict())

    #Add code to order them

    if len(users_dicts) > 5:
        users_dicts = users_dicts[:5]

    return users_dicts