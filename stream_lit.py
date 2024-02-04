import requests
import streamlit as st

# Page title
st.set_page_config(page_title='Txt File Summarization')
st.title('Txt File Summarization Demo')

# # Upload button
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

with st.form('summarize_form', clear_on_submit=False):
    if uploaded_file: 
        file_contents = uploaded_file.getvalue().decode("utf-8")
        st.text_area("File Contents", file_contents, height=250) 
    
    submitted = st.form_submit_button('Upload and Summarize')
    if submitted:
        with st.spinner('Calculating...'):
            payload = {"file": uploaded_file.name}
            response = requests.post("http://localhost:8000/upload",params=payload, files={"file": uploaded_file.getvalue()})
            if response.status_code == 200:
                st.info(response.text)
            else:
                st.error(response.text)
