from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import click, pickle, os,sys

def refresh_creds():
    creds = None
    info = []
    try:
        with open('lib/firebase-creds.txt', 'r') as user_info:
            for line in user_info:
                info.append(line.strip())  
        
    except FileNotFoundError:
        return None
    
    if len(info) == 0:
        os.remove('lib/firebase-creds.txt')
        sys.exit("Please login")

    if os.path.exists(f'{info[0]}.pickle'):
        with open(f'{info[0]}.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        click.secho("You are not yet registered.")
        return None

    if  not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    service = build('calendar', 'v3', credentials=creds)
    
    return service