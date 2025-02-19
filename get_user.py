import os,click

def get_user(db):
    if not os.path.exists('lib/firebase-creds.txt'):
        click.secho("You are not logged in", fg="red")
        return
        
    info = []
    try:
        with open('lib/firebase-creds.txt', 'r') as user_info:
            for line in user_info:
                info.append(line.strip())
        
        user_ref = db.collection('users').document(info[0])
        user_snapshot = user_ref.get()
        if user_snapshot.exists:
            return user_snapshot.to_dict() 
        return None
    except:
        return None
    