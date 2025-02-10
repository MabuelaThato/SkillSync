def get_users(role):
    if not os.path('lib/firebase-creds.txt'):
        click.echo("You are not logged in")
        return
        
    docs = db.collection('users').where('role', '==', role).stream()

    users_dicts = []

    for doc in docs:
        users_dicts.append(doc.to_dict())
    
    return users_dicts
