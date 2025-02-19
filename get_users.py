import os,click

def get_users(role,db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
        
    docs = db.collection('users').where('role', '==', role).stream()

    users_dicts = []

    for doc in docs:
        users_dicts.append(doc.to_dict())
    
    return users_dicts
