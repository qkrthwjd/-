from pydantic import BaseModel
import classifier
import FAQ
import NORMAL
import unidentified
import report
import real_report
import FAC
import non_ex_classroom
from fastapi import FastAPI, Request, Header
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
# Firebase Admin SDK 초기화
cred = credentials.Certificate('sanhak-45ec5-firebase-adminsdk-1q65g-b21cc8ae9c.json')  # Firebase 서비스 계정 키 파일 경로
firebase_admin.initialize_app(cred)
db = firestore.client()
# uvicorn main:app --reload --port 5000
# ngrok http --domain=beetle-prompt-finally.ngrok-free.app 5000
# https://beetle-prompt-finally.ngrok-free.app
app = FastAPI()


@app.get("/")
async def read_root():
    return {"2024 SKKU SWE PROJECT"}

app = FastAPI()

class BodyModel(BaseModel):
    text: str
    FAQ_id: str

class ErrorModel(BaseModel):
    code: int
    message: str

@app.post("/chat/")
async def receive_json(body: BodyModel, token: Optional[str] = Header(None)):
    if token is None:
        raise HTTPException(status_code=400, detail="Token header missing")
    
    # 토큰 출력
    print(f"Received token: {token}")
    #print(body.text)
    #print(body.FAQ_id)
    if(body.FAQ_id!=""):
        FAQ.append_to_chat_history(token, body.FAQ_id, db)
        return{
            "answerType":"FAQ",
            "text" : "",
            "FAQ_id" : "",
            "data": None
        }
    else:
        chat_type = classifier.chat_type_classifier(body.text)
        if chat_type=="NORMAL":
            response = NORMAL.append_to_chat_history(token, body.text, db)
            return{
            "answerType":"NORMAL",
            "text" : response,
            "FAQ_id" : "",
            "data": None
        }
        elif chat_type=="unidentified":
            response = unidentified.append_to_chat_history(token,body.text, db)
            return{
            "answerType":"NORMAL",
            "text" : response,
            "FAQ_id" : "",
            "data": None
        } 
        elif chat_type=="MY_REPORT":
            return{
            "answerType":"MY_REPORT",
            "text" : "",
            "FAQ_id" : "",
            "data": None
        }
        elif chat_type=="report":
            response = report.append_to_chat_history(token, body.text, db)
            return{
            "answerType":"NORMAL",
            "text" : response,
            "FAQ_id" : "",
            "data": None
        }
        elif chat_type=="real_report":
            classroom, item = real_report.AIresponse(body.text)
            return{
            "answerType":"REPORT",
            "text" : "",
            "FAQ_id" : "",
            "data": {
                "classroom": classroom,
                "broken_item": item
            }
        }
        elif chat_type=="FAC":
            response, classroom= FAC.append_to_chat_history(body.text, body.text, db)
            if response == "":
              return{
                "answerType":"FAC",
                "text" : "",
                "FAQ_id" : "",
                "data": {
                    "classroom": classroom
                }
              }
            else:
                return{
                "answerType":"NORMAL",
                "text" : response,
                "FAQ_id" : "",
                "data": None
              }
        else:
            response = unidentified.append_to_chat_history(token,body.text, db)
            return{
            "answerType":"NORMAL",
            "text" : response,
            "FAQ_id" : "",
            "data": None
        } 


@app.post("/error/")
async def receive_json(body: ErrorModel, token: Optional[str] = Header(None)):
    if token is None:
        raise HTTPException(status_code=400, detail="Token header missing")
    
    print(f"Received token: {token}")
    if body.code == 400:
        response = non_ex_classroom.append_to_chat_history(token, db)
        return{
                "answerType":"NORMAL",
                "text" : response,
                "FAQ_id" : "",
                "data": None
            } 
    else: 
        return{
                "answerType":"NORMAL",
                "text" : "backend error",
                "FAQ_id" : "",
                "data": None
            } 