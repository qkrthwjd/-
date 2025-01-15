import firebase_admin
from firebase_admin import credentials, firestore
from doctest import Example
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

classifier_llm = ChatOpenAI(model="gpt-3.5-turbo-0125",api_key="sk-proj-ord3wqZDvZj48Y4lAdBQT3BlbkFJbgoZjkwuSLILu72PNMYc", temperature=0.0)


def chat_type_classifier(chat):

    examples = [
    {"input": "강의실 조회", "output": "classroom_err"}, 
    {"input": "강의실 조회", "output": "classroom_err"}
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
        ("system", "너는 성균관대학교 시설물관리 어플 인공지능이야. 채팅에 따라 일어난 오류의 종류를 알려줘"),
        few_shot_prompt,
        ("human", "{input}"),
    ]
    )

    chain = final_prompt | classifier_llm
    result = chain.invoke({"input": chat}).content
    print(result)
    return result



def append_to_chat_history(user_token: str, text: str, db):
    print(f"오류 텍스트:{text}")
    type = chat_type_classifier(text)
    if type =='classroom_err':
        response = '''강의실 조회를 원하신다면 다음과 같은 형식으로 말씀해주세요
\"OOOOO강의실 조회\"'''
    else :
        response = '해당 요청은 인공지능이 이해할 수 없습니다'
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



