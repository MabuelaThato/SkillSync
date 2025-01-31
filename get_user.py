def get_user(db):
    info = []
    try:
        with open('lib/firebase-creds.txt', 'w') as user_info:
            for line in user_info:
                info.append(line.strip())
        
        user = db.collection('users').document(info[0])
        return user
    except:
        return None
    