import firebase_admin
from firebase_admin import credentials, firestore
from doctest import Example
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
import re

classifier_llm = ChatOpenAI(model="gpt-3.5-turbo-0125",api_key="sk-proj-ord3wqZDvZj48Y4lAdBQT3BlbkFJbgoZjkwuSLILu72PNMYc", temperature=0.0)

def extract_info(response):
    # Regular expression to match the pattern of the response
    pattern = r"(\d{5})\s(.+)"
    match = re.match(pattern, response)
    if match:
        classroom_number = match.group(1)
        item_name = match.group(2)
        return classroom_number, item_name
    else:
        return None, None

#핵심부===============================================================================================
def AIresponse(chat):
    examples = [
    {"input": "26302강의실 전등 신고", "output": "26302 전등"}, 
    {"input": "31062강의실 콘센트", "output": "31062 콘센트"},
    {"input": "33012 에어컨", "output": "33012 에어컨"},
    {"input": "26312강의실 의자 신고", "output": "26312 의자"},
    {"input": "26001강의실 의자", "output": "26001 의자"}
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
        ("system", "너는 성균관대학교 시설물관리 어플 인공지능이야. 사용자들의 신고하고자하는 강의실 번호와 물건 이름을 말해줘"),
        few_shot_prompt,
        ("human", "{input}"),
    ]
    )

    chain = final_prompt | classifier_llm

    classroom, item = extract_info(chain.invoke({"input": chat}).content)
    return classroom, item
#핵심부===============================================================================================

def append_to_chat_history(user_token: str, text: str, db):
    classroon_num, item = AIresponse(text)
    chathistory = f'''
[user] {text}
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
        return classroon_num, item
    else:
        # Create a new document with the initial chat history
        doc_ref.set({
            'chathistory': chathistory
        })
        print(f"Created new document for token {user_token} with initial chat history.")
        return classroon_num, item



