import firebase_admin
from firebase_admin import credentials, firestore
from doctest import Example
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
import re

classifier_llm = ChatOpenAI(model="gpt-3.5-turbo-0125",api_key="sk-proj-ord3wqZDvZj48Y4lAdBQT3BlbkFJbgoZjkwuSLILu72PNMYc", temperature=0.0)

#핵심부===============================================================================================
def AIresponse(chat):
    examples = [
    {"input": "26302강의실 조회", "output": "26302"}, 
    {"input": "31062강의실", "output": "31062"},
    {"input": "33012", "output": "33012"},
    {"input": "26312강의실 정보", "output": "26312"},
    {"input": "26001강의실 의자", "output": "26001"}
    ]

    # This is a prompt template used to format each individual example.
    example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
    )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 성균관대학교 시설물관리 어플 인공지능이야. 사용자들의 정보 조회를 하려는 강의실 번호를 말해줘"),
        few_shot_prompt,
        ("human", "{input}"),
    ]
    )

    chain = final_prompt | classifier_llm
    return chain.invoke({"input": chat}).content
    
#핵심부===============================================================================================
def append_to_chat_history(user_token: str, text: str, db):
    result = AIresponse(text)
    if result.isdigit() and 4 <= len(result) <= 5:
        response = ""
        chathistory = f'''
[user] {text}
'''
    else:
        response = '''강의실 조회를 원하신다면 다음과 같은 형식으로 말씀해주세요
\"OOOOO강의실 조회\"'''
    chathistory = f'''
[user] {text}
[AI] {response}
'''
    print(f"강의실 조회{response} {result}")
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
        return response, result
    else:
        # Create a new document with the initial chat history
        doc_ref.set({
            'chathistory': chathistory
        })
        print(f"Created new document for token {user_token} with initial chat history.")
        return response, result



