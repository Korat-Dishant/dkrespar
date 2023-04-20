# import textract 

def read_docx(path):
   
    try:
        try:
            import textract
        except ImportError:
            return ' import error '
        temp = textract.process(path).decode('utf-8')
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    except KeyError:
        return ' key errrr'
    
    
def main():
    path = "    "
    print(read_docx(path))

if __name__ == "__main__":
    main()