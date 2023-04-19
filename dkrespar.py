import spacy 
# from spacy import displacy  to render text with entities
import pandas as pd

from pdf_to_text import read_pdf
from docx_to_text import read_docx
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import PyPDF2
import os
import tempfile


import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools



def readby_id_pdf(pdf_id):
    """
    arguments => id of pdf stored in google drive
    return => text extracte from pdf  

    """
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    # create GoogleDrive instance and get file by ID
    drive = GoogleDrive(gauth)
    file_id = str(pdf_id)
    file = drive.CreateFile({'id': file_id})
    # download the file to a temporary location
    temp_file_path = os.path.join(tempfile.gettempdir(), file['title'])
    file.GetContentFile(temp_file_path)
    # extract the text from the PDF file
    text = ""
    with open(temp_file_path, 'rb') as f:
        pdf_file = PyPDF2.PdfReader(f)
        for page in range(len(pdf_file.pages)):
            page_obj = pdf_file.pages[page]
            text += page_obj.extract_text()
    # delete the temporary file
    os.remove(temp_file_path)
    return text





SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
def get_credentials():
    store = file.Storage('token.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials
def read_paragraph_element(element):
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')
def read_structural_elements(elements):
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text

def readby_id_doc(doc_id):
    global DOCUMENT_ID
    DOCUMENT_ID = str(doc_id)
    """Uses the Docs API to print out the text of a document."""
    credentials = get_credentials()
    http = credentials.authorize(Http())
    docs_service = discovery.build(
        'docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    text = ""
    text += str(read_structural_elements(doc_content))
    return text





df = pd.read_csv("data/skills.csv")
skl = list(df.columns)


nlp = spacy.blank("en")

ruler = nlp.add_pipe("entity_ruler")
patterns = []

for skill in skl:
    patterns.append({"label": "SKILL", "pattern": skill})

ruler.add_patterns(patterns)


def extract_data(url):
    # to access file locally using local path 
    # file_name, file_extension = os.path.splitext(path)
    # if file_extension == ".pdf":
    #     text = read_pdf(path)
    # if file_extension == ".docx":
    #     text = read_docx(path)
    
    url_lst = url.split("/")
    if url_lst[3] == "document" :
        text = readby_id_doc(url_lst[5])
    if url_lst[3] == "file" :
        text = readby_id_pdf(url_lst[5])

    doc = nlp(text.lower())
    extracted_skills = []
    for j in doc.ents :
        extracted_skills.append(j)
    return extracted_skills




# for testing 
# print(extract_data("https://drive.google.com/file/d/1U0lGu-fa7B7BlSCEZOShAph8U6p3zC7B/view"))