from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm_model import get_llm
from app.main import InputQA, OutputQA, load_new_pdf, build_rag_chain, delete_file_by_metadata, load_new_pdfs, get_metadata
import os
from dotenv import load_dotenv
from typing import List
import jwt
from typing import Union, Any
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from huggingface_hub import login

load_dotenv()
llm = get_llm(temperature = 0.01)
genai_docs_env = os.getenv("GENAI_DOCS")
#upload_dir_env = os.getenv("UPLOAD_DIR")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
genai_chain = build_rag_chain(llm, data_dir = genai_docs_env ,use_reranking= True)


class DeleteRequest(BaseModel):
    value: str

app = FastAPI(
    title= "Langchain Server",
    version="1.0",
    description="Simple api server using Langchain's interfaces",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    expose_headers = ["*"],
)
def verifyLogin(username, password):
    if username == 'admin' and password =="1":
        return True
    else:
        return False

def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 0.5  
    )
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class LoginRequest(BaseModel):
    username: str
    password: str


@app.post('/login')
def login(request: LoginRequest):
    print(f'[x] request_data: {request.__dict__}')
    if verifyLogin(username=request.username, password=request.password):
        token = generate_token(request.username)
        return {
            'token': token
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/check")
async def check():
    return {"Status" : "ok" }

@app.post("/upload_file") #dependencies=[Depends(validate_token)]
async def upload(uploadfiles:List[UploadFile] = File(...)):
    uploaded_filenames =[]
    for uploadfile in uploadfiles:
        file_path = os.path.join(genai_docs_env, uploadfile.filename)
        with open(file_path, "wb") as f:
            f.write(await uploadfile.read())             # Save file
        #load_new_pdf(upload_dir_env)
        vector_embedding = load_new_pdf(data_dir=genai_docs_env)
        print('Vector_embedding: ' , vector_embedding)
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
        uploaded_filenames.append(uploadfile.filename) 
    return {"message": f"Successfully uploaded files: {', '.join(uploaded_filenames)}"}

@app.post("/generative_ai", response_model=OutputQA)
async def generative_ai(inputs: InputQA):
    answer = genai_chain.invoke(inputs.question)
    print(f"Raw output: {answer} (type: {type(answer)})")
    if callable(answer):  
        answer = answer()
    if not isinstance(answer, str):
        answer = str(answer)
    answer = answer.strip()
    return {"answer": answer}

# @app.post("/generative_ai_new", response_model=OutputQA)
# async def generative_ai(inputs: InputQA):
#     answer = genai_chain_new.invoke(inputs.question)
#     print(f"Raw output: {answer} (type: {type(answer)})")
#     if callable(answer):  
#         answer = answer()
#     if not isinstance(answer, str):
#         answer = str(answer)
#     answer = answer.strip()
#     return {"answer": answer}

@app.delete("/delete_file") #, dependencies=[Depends(validate_token)]
async def delete_by_metadata(delete_request: DeleteRequest):

        delete = delete_file_by_metadata(data_dir=genai_docs_env, filename= delete_request.value)
        if delete:
            return {"message": f"Deleted documents with metadata {delete_request.value}."}
        else: print ("message:" "Error deleting documents")


@app.get("/print_metadata") #, dependencies=[Depends(validate_token)]
async def print_metadata():
    data = get_metadata(data_dir = genai_docs_env)
    if data:
        print(data)
        return {"message": [r.strip() if isinstance(r, str) else r for r in data]}
    else: print ("message:" "Error deleting documents") 


# @app.post("/generative_ai", response_model=OutputQA)
# async def generative_ai(inputs: InputQA):
#     # input_data = {
#     #     "question": inputs.question
#     #     config = {
#     #         "con"
#     #     }
#     # }
#     answer = genai_chain.invoke(
#         {"question": inputs.question})["answer"]
#     # input_data = {
#     #     "question": inputs.question,
#     #     "chat_history": chat_history
#     # }
#     #answer = genai_chain.invoke(input_data)
#     #print(f"Lịch sử trò chuyện: {chat_history}")
#     print(f"Raw output: {answer} (type: {type(answer)})")
#     if callable(answer):  
#         answer = answer()
#     if not isinstance(answer, str):
#         answer = str(answer)
#     answer = answer.strip()
#     # chat_history.append(inputs.question)
#     # chat_history.append(answer)
#     # print(chat_history)
#     return {"answer": answer}

add_routes(app, genai_chain, playground_type="default",path="/generative_ai")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)