import streamlit as st
from google.cloud import firestore

import google.oauth2.credentials
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-reddit")


# Streamlit widgets to let a user create a new post
title = st.text_input('Post Title')
url = st.text_input('Post URL')
submit = st.button('Submit New Post')

# Once the user has submitted the post, add it to Firestore
if title and url and submit:
    doc_ref = db.collection('posts').document(title)
    doc_ref.set({
        "title": title,
        "url": url,
    })
    
# And then render each post, using some light Markdown formatting
posts_ref = db.collection('posts')
for doc in posts_ref.stream():
    post = doc.to_dict()
    title =  post['title']
    url = post["url"]
    
    st.subheader(f"Post: {title}")
    st.write(f":link: [{url}]({url})")