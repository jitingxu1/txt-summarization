import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(txt):
    """
    Generate a text summary using OpenAI API.

    Args:
        txt (str): The text to be summarized.

    Returns:
        str: The generated text summary.
    """
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt)
    docs = [Document(page_content=t) for t in texts]
    # Text summarization
    chain = load_summarize_chain(llm, chain_type='map_reduce')
    return chain.run(docs)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class Response(BaseModel):
    summary: str

@app.get("/")
async def health():
    return {"message": "Hello World!"}

@app.post("/upload")
@limiter.limit("2/minute")
async def upload(request: Request,file: UploadFile = File(...)):  
    try:
        contents = await file.read()
        txt = contents.decode("utf-8")
        summary = generate_summary(txt)
    except RateLimitExceeded:
        return {"message": "Rate limit exceeded for this IP address. Please try again later."}
    except Exception:
        return {"message": "There was error uploading the file"}
    finally:
        file.close()

    return Response(summary=summary)