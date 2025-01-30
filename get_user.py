def get_user():
    info = []
    try:
        with open('lib/firebase-creds.txt', 'w') as user_info:
            for line in user_info:
                info.append(line.strip())
    
    return info