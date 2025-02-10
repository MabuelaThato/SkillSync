def get_user(db):
    if not os.path('lib/firebase-creds.txt'):
        click.echo("You are not logged in")
        return
        
    info = []
    try:
        with open('lib/firebase-creds.txt', 'w') as user_info:
            for line in user_info:
                info.append(line.strip())
        
        user = db.collection('users').document(info[0])
        return user.get()
    except:
        return None
    