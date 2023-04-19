from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import PyPDF2
import os
import tempfile


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

def main():
    # in case some error accur in code just delete the mycreds.txt and rerun the code 
    #  for test purpose 
    PDF_ID_HERE = "1U0lGu-fa7B7BlSCEZOShAph8U6p3zC7B"
    print(readby_id_pdf(PDF_ID_HERE))


if __name__ == "__main__":
    main()
