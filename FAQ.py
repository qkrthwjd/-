
chat1 = ''' 
[user] FAQ1
[AI] FAQ1
'''
chat2 = '''
[user] FAQ2
[AI] FAQ2
'''
chat3 = '''
[user] FAQ3
[AI] FAQ3
'''
chat4 = '''
[user] FAQ4
[AI] FAQ4
'''
chat5 = '''
[user] FAQ5
[AI] FAQ5
'''
chat6 = '''
[user] FAQ6
[AI] FAQ6
'''
chat_dict = {'id1':chat1, 'id2':chat2, 'id3':chat3, 'id4':chat4}

import firebase_admin
from firebase_admin import credentials, firestore


def append_to_chat_history(user_token: str, FAQ_id: str, db):
    # Reference to the document
    doc_ref = db.collection('chatbot_users').document(user_token)

    # Get the document
    doc = doc_ref.get()
    if doc.exists:
        # Get the existing chat history
        chat_history = doc.to_dict().get('chathistory', '')
        
        # Append the new text to the chat history
        updated_chat_history = chat_history + chat_dict[FAQ_id]

        # Update the document with the new chat history
        doc_ref.update({
            'chathistory': updated_chat_history
        })
        print(f"Updated chat history for token {user_token}.")
    else:
        # Create a new document with the initial chat history
        doc_ref.set({
            'chathistory': chat_dict[FAQ_id]
        })
        print(f"Created new document for token {user_token} with initial chat history.")



