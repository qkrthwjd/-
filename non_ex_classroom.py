import firebase_admin
from firebase_admin import credentials, firestore


def append_to_chat_history(user_token: str, db):
    response = '존재하지 않는 강의실 번호입니다. '
    chathistory = f'''
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



