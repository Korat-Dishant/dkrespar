import spacy 
# from spacy import displacy  to render text with entities
import pandas as pd

from pdf_to_text import read_pdf
from docx_to_text import read_docx
import os

from google_drive.doc.read_docs import readby_id_doc
from google_drive.pdf.read_pdf import readby_id_pdf


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
extract_data("https://drive.google.com/file/d/1U0lGu-fa7B7BlSCEZOShAph8U6p3zC7B/view")