import re
import arxiv
import dropbox
from dropbox.exceptions import AuthError
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Access Dropbox access token
access_token = os.environ.get("DROPBOX_ACCESS_TOKEN")

# Construct the default API client.
client = arxiv.Client()

# Get the user interest
with open('interest.json', 'r') as f:
    data = json.load(f)
    interests = data['interests']

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
 query=interests,
 max_results=10,
 sort_by=arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)

# Initialize Dropbox client
try:
    dbx = dropbox.Dropbox(access_token)
except AuthError as e:
    print(f"Error connecting to Dropbox: {e}")
    exit()

def sanitize(id):
    # Remove any characters not allowed in Dropbox file names
    return re.sub(r'[<>:"/\\|?*]', '', id)

# Function to upload file to Dropbox
def upload_to_dropbox(file_path, dropbox_path):
    with open(file_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path)

# Download and upload each paper
for r in results:
    # Download the paper
    pdf_path = r.download_pdf()

    # Sanitize
    id = sanitize(r.get_short_id())
    
    # Construct the Dropbox path
    dropbox_path = f"/LLM/{id}.pdf"
    
    # Upload the file to Dropbox
    upload_to_dropbox(pdf_path, dropbox_path)
    print(f"Uploaded {id} to Dropbox")

    # Delete from local system
    os.remove(pdf_path)
