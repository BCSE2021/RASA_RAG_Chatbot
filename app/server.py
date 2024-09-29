from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_model import get_llm
from main import InputQA, OutputQA, load_new_pdf, build_rag_chain, delete_file_by_metadata
import os
from dotenv import load_dotenv
from typing import List


load_dotenv()
llm = get_llm(temperature = 0.9)
genai_docs_env = os.getenv("GENAI_DOCS")
upload_dir_env = os.getenv("UPLOAD_DIR")
genai_chain = build_rag_chain(llm, data_dir = genai_docs_env ,use_reranking= True)
genai_chain_new = load_new_pdf(llm, data_dir = genai_docs_env, data_type="pdf")

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

@app.get("/check")
async def check():
    return {"Status" : "ok" }

@app.post("/upload_file")
async def upload(uploadfiles:List[UploadFile] = File(...)):
    uploaded_filenames =[]
    for uploadfile in uploadfiles:
        file_path = os.path.join(upload_dir_env, uploadfile.filename)
        with open(file_path, "wb") as f:
            f.write(await uploadfile.read())             # Save file to server
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

@app.post("/generative_ai_new", response_model=OutputQA)
async def generative_ai(inputs: InputQA):
    answer = genai_chain_new.invoke(inputs.question)
    print(f"Raw output: {answer} (type: {type(answer)})")
    if callable(answer):  
        answer = answer()
    if not isinstance(answer, str):
        answer = str(answer)
    answer = answer.strip()
    return {"answer": answer}

@app.delete("/delete_file")
async def delete_by_metadata(delete_request: DeleteRequest):
    #try:
        delete = delete_file_by_metadata(data_dir=genai_docs_env, filename= delete_request.value)
        if delete:
            return {"message": f"Deleted documents with metadata {delete_request.value}."}
        else: print ("message:" "Error deleting documents")
        
    #except Exception as e:
       # raise HTTPException(status_code=500, detail=f"Error deleting documents: {str(e)}")


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