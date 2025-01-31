def get_users(role):
    docs = db.collection('users').where('role', '==', role).stream()

    users_dicts = []

    for doc in docs:
        users_dicts.append(doc.to_dict())
    
    return users_dicts
