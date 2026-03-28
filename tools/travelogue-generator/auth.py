import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Use the new Picker API scope
SCOPES = ['https://www.googleapis.com/auth/photospicker.mediaitems.readonly']

def get_credentials():
    """Shows basic usage of the Photos v1 API.
    Prints the names and ids of the first 10 albums the user has access to.
    """
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Please download OAuth 2.0 client ID credentials from Google Cloud Console and save them as {creds_path} in the same directory.")
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False, prompt='consent')
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds
