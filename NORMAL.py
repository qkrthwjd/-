import firebase_admin
from firebase_admin import credentials, firestore
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
import torch
from deep_translator import GoogleTranslator
import base64
import requests

# OpenAI API Key
api_key = "sk-proj-ord3wqZDvZj48Y4lAdBQT3BlbkFJbgoZjkwuSLILu72PNMYc"

#핵심부===============================================================================================
def AIresponse(user_token, text, db):
    doc_ref = db.collection('chatbot_users').document(user_token)
    doc = doc_ref.get()
    chat_history = 'no chat history '
    if doc.exists:
        # Get the existing chat history
        chat_history = doc.to_dict().get('chathistory', '')
    
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f'''다음은 성균관대학교에서 개발한 시설물 관리 어플리케이션 사용법을 알려주는 인공지능이야. 
            간결하게 대답해줘. 그리고 대답에서 "*" 기호를 사용하지 말아줘.
            그리고 사용자에게 하드웨어나 서버에대한 설명은 하지 말아줘.
            다음은 지금까지 우리의 대화야
            {chat_history}
            이 문서들을 토대로 다음과 같은 사용자의 물음에 짧게 답변을 해줘
            [사용자] {text}'''
            },
            {
            "type": "image_url",
            "image_url": {
                "url": "https://raw.githubusercontent.com/beefed-up-geek/images/main/Fix-SKKU/1.PNG"
            }
            },
            {
            "type": "image_url",
            "image_url": {
                "url": "https://raw.githubusercontent.com/beefed-up-geek/images/main/Fix-SKKU/2.PNG"
            }
            },
            {
            "type": "image_url",
            "image_url": {
                "url": "https://raw.githubusercontent.com/beefed-up-geek/images/main/Fix-SKKU/3.PNG"
            }
            }
        ]
        }
    ],
    "max_tokens": 300,
    "temperature": 1
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # print(response.json()['choices'][0]['message']['content'])
    return response.json()['choices'][0]['message']['content']
#핵심부===============================================================================================
def append_to_chat_history(user_token: str, text: str, db):
    response = AIresponse(user_token, text, db)
    chathistory = f'''
[user] {text}
[AI] {response}
'''
    doc_ref = db.collection('chatbot_users').document(user_token)

    # Get the document
    doc = doc_ref.get()
    if doc.exists:
        # Get the existing chat history
        chat_history = doc.to_dict().get('chathistory', '')
        
        # Append the new text to the chat history
        updated_chat_history = chat_history + chathistory

        # Update the document with the new chat history
        doc_ref.update({
            'chathistory': updated_chat_history
        })
        print(f"Updated chat history for token {user_token}.")
        return response
    else:
        # Create a new document with the initial chat history
        doc_ref.set({
            'chathistory': chathistory
        })
        print(f"Created new document for token {user_token} with initial chat history.")
        return response



