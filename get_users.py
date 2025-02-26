import os,click

def get_users(role,db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
        
    docs = db.collection('users').stream()

    users_dicts = []

    for doc in docs:
        doc = doc.to_dict()
        if role == 'all':
            users_dicts.append(doc)
        else:
            if doc["role"] == role:
                users_dicts.append(doc)
    
    return users_dicts
