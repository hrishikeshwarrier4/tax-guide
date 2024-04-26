#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 02:18:01 2024

@author: hrishikeshwarrier
"""

import os
import openai

import streamlit as st
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

st.title("TaxMate: Smart Solutions for Smart Taxpayers!")

st.write("Here are some queries you can ask for a start:")
st.write("Who needs to file taxes?")
st.write("What's the deadline for tax filing?")
st.write("I got married last year. How does this affect my tax filing?")
st.write("I made a mistake on my tax return last year. How do I fix it?")

# Configure API keys and directories
openai.api_key = 'OPENAI_API_KEY'
os.environ['OPENAI_API_KEY'] = openai.api_key
documents_path = 'path/to/directory/'  # Path where your tax-related documents are stored
vector_storage_path = "chroma_db"  # Path for storing Chroma database files

# Load PDF documents from a specified directory
def load_tax_documents(directory: str):
    loader = PyPDFDirectoryLoader(directory)
    tax_documents = loader.load()
    return tax_documents

# Split documents into manageable text chunks
def chunk_tax_documents(tax_documents, max_chunk_size=1000, overlap_size=20):
    splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=overlap_size)
    chunked_documents = splitter.split_documents(tax_documents)
    return chunked_documents

# Initialize and store models and databases on startup
def initialize_resources():
    if 'vector_db' not in st.session_state or 'qa_chain' not in st.session_state:
        tax_documents = load_tax_documents(documents_path)
        document_chunks = chunk_tax_documents(tax_documents)

        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_database = Chroma.from_documents(
            documents=document_chunks,
            embedding=embeddings,
            persist_directory=vector_storage_path
        )
        vector_database.persist()

        model_name = "gpt-3.5-turbo"
        llm_model = ChatOpenAI(model_name=model_name)
        qa_chain = load_qa_chain(llm_model, chain_type="stuff", verbose=True)

        st.session_state['vector_db'] = vector_database
        st.session_state['qa_chain'] = qa_chain
        return vector_database, qa_chain
    else:
        return st.session_state['vector_db'], st.session_state['qa_chain']

# Handle chat interactions and retrieve answers based on user queries
def process_user_query(query: str, vector_db, qa_chain):
    documents_with_scores = vector_db.similarity_search_with_score(query)
    relevant_documents = [doc for doc, score in documents_with_scores]
    answer_result = qa_chain.run(input_documents=relevant_documents, question=query)
    return {"answer": answer_result}

# Initialize and manage the chatbot interface
def launch_tax_chatbot():
    vector_db, qa_chain = initialize_resources()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if user_input := st.chat_input("How can I assist you with your tax queries today?"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = process_user_query(st.session_state.chat_history[-1]["content"], vector_db, qa_chain)
            response_text = response['answer']
            message_placeholder.markdown(response_text)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

# Start the chatbot application
if __name__ == '__main__':
    launch_tax_chatbot()
