import streamlit as st
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext
from llama_index.llms.ollama import Ollama
import subprocess

# Title
st.title("Marketing AI Assistant")

# File uploader
uploaded_files = st.file_uploader("Upload documents", type=["txt", "pdf", "docx"], accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        with open(f"./docs/{file.name}", "wb") as f:
            f.write(file.getbuffer())
    st.success("Files uploaded successfully! Click below to re-index.")
    if st.button("Rebuild Index"):
        subprocess.run(["python", "ingest.py"])
        st.success("Index rebuilt successfully.")

# Load the index
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)

# Query engine
query_engine = index.as_query_engine(llm=Ollama(model="llama2"))

# Chat interface
query = st.text_input("Ask a question about your files:")
if query:
    response = query_engine.query(query)
    st.write(response.response)
    
st.markdown("---")
st.header("AI Content Generator")

# Content type selection
content_type = st.selectbox("Choose content type", [
    "Social Media Post", 
    "Email Marketing", 
    "Product Description", 
    "Ad Headline", 
    "Landing Page Copy"
])

# Description input
description = st.text_area("Describe your product, offer, or idea:")

# Refine prompt function
def refine_prompt(description, content_type):
    if content_type == "Email Marketing":
        return f"Write a professional, persuasive marketing email for the following: {description}"
    elif content_type == "Social Media Post":
        return f"Write a catchy and engaging social media post for the following: {description}"
    elif content_type == "Product Description":
        return f"Write a detailed, compelling product description for the following: {description}"
    else:
        return f"Write content for the following: {description}"

# Handle content generation
if st.button("✨ Generate Content"):
    if description:
        refined_prompt = refine_prompt(description, content_type)  # Now we call refine_prompt here
        with st.spinner('Generating content...'):
            response = query_engine.query(refined_prompt)
            st.subheader("Generated Content:")
            st.write(response.response)
    else:
        st.warning("Please enter a description first.")
