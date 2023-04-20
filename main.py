from fastapi import FastAPI
from dkrespar import extract_data

# print(extract_data("https://drive.google.com/file/d/1U0lGu-fa7B7BlSCEZOShAph8U6p3zC7B/view"))

app = FastAPI(title="dkrespar",description="API to extract skills from resume link uploaded on drive")

@app.post("/extract", summary="extract skills", tags=["dkrespar"])
def extract(data: str) -> str:
        return str(extract_data(data))

@app.get("/")
async def index():
   return {"message": "Hello World uses //extract for api"}

# print(extract_data("https://docs.google.com/document/d/13wh5v5_5eSQH6-OMVaNC4T2KfqJKYviJdi5R-RDftZI/edit"))