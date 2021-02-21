from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
# from gdoctableapppy import gdoctableapp

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive"]

# comment below code if you want same number of row and col EVERYtime
row = int(input("Enter Row :"))
col = int(input("Enter Col :"))  
# row = Remove_me_and_type_Number_of_row
# col = Remove_me_and_type_Number_of_COL
 
folder_id = "Enter Folder ID"

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)
    serviceDoc = build("docs", "v1", credentials=creds)
    # Call the Drive v3 API
    # Create Google Docs file in folder

    
    file_metadata = {
    "name": sys.argv[1], 
    "mimeType":'application/vnd.google-apps.document',
    "parents": [folder_id],
    }

    file = service.files().create(body=file_metadata, fields="id").execute()
    print("File ID: %s" % file.get("id"))

    DOCUMENT_ID = file.get("id")

    requests = [{"insertTable": {"rows": row, "columns": col, "location": {"index": 1}}}]

    result = (
        serviceDoc.documents()
        .batchUpdate(documentId=DOCUMENT_ID, body={"requests": requests})
        .execute()
    )
    return


if __name__ == "__main__":
    main()
