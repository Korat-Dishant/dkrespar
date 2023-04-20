from PyPDF2 import PdfReader

def read_pdf(path):
    pdf = PdfReader(path)
    text = ""
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]  
        text += page.extract_text()
    return text

def main():
    path = "    "
    print(read_pdf(path))

if __name__ == "__main__":
    main()