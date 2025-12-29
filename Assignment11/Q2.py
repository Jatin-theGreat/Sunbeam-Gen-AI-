import chromadb
import os
from langchain.embeddings import init_embeddings
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
st.set_page_config(page_title="Resume Details", layout="wide")
embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy",
    check_embedding_ctx_length=False
)
db = chromadb.PersistentClient(path="./Resume_data")
collection = db.get_or_create_collection("resumes")
def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text = ""
    for page in docs:
        text += page.page_content
    return text
if "loaded" not in st.session_state:
    if os.path.exists("fake-resumes"):
        for file in os.listdir("fake-resumes"):
            if file.endswith(".pdf"):
                resume_name = file
                full_path = os.path.abspath(os.path.join("fake-resumes", file))
                if resume_name not in collection.get()["ids"]:
                    resume_text = load_pdf_resume(full_path)
                    embedding = embed_model.embed_documents([resume_text])
                    collection.add(
                        ids=[resume_name],
                        documents=[resume_text],
                        embeddings=embedding,
                        metadatas=[{"source": full_path}]
                    )
    st.session_state.loaded = True
st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Add", "Delete", "Update", "All Resumes"]
)
all_ids = collection.get()["ids"]
if page == "Home":
    st.title("Resume Search")
    query = st.text_input("Ask Anything.....")
    if query:
        q_embed = embed_model.embed_query(query)
        result = collection.query(query_embeddings=[q_embed], n_results=1)
        if result["documents"][0]:
            st.subheader("Matched Resume Text")
            st.write(result["documents"][0])
            st.subheader("Metadata")
            st.write(result["metadatas"][0])
        else:
            st.info("No matching resume found")
elif page == "Add":
    st.title("Add Resume")
    uploaded_pdf = st.file_uploader("Upload Resume PDF", type=["pdf"])    
    if uploaded_pdf and st.button("Add Resume"):
        resume_name = uploaded_pdf.name
        temp_path = os.path.abspath(resume_name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_pdf.read())
        resume_text = load_pdf_resume(temp_path)
        embedding = embed_model.embed_documents([resume_text])
        if resume_name not in all_ids:
            collection.add(
                ids=[resume_name],
                documents=[resume_text],
                embeddings=embedding,
                metadatas=[{"source": temp_path}]
            )
            st.success(f"{resume_name} added successfully")
        else:
            st.warning(f"{resume_name} already exists!")
        os.remove(temp_path)
        st.rerun()
elif page == "Delete":
    st.title("Delete Resume")
    if all_ids:
        delete_id = st.selectbox("Select resume", all_ids)
        if st.button("Delete Resume"):
            collection.delete(ids=[delete_id])
            st.success(f"{delete_id} deleted successfully")
            st.rerun()
    else:
        st.info("No resumes available to delete")
elif page == "Update":
    st.title("Update Resume")
    if all_ids:
        update_id = st.selectbox("Select resume", all_ids)
        updated_pdf = st.file_uploader("Upload updated PDF", type=["pdf"])
        if updated_pdf and st.button("Update Resume"):
            temp_path = os.path.abspath(updated_pdf.name)
            with open(temp_path, "wb") as f:
                f.write(updated_pdf.read())
            new_text = load_pdf_resume(temp_path)
            new_embedding = embed_model.embed_documents([new_text])
            collection.delete(ids=[update_id])
            collection.add(
                ids=[update_id],
                documents=[new_text],
                embeddings=new_embedding,
                metadatas=[{"source": temp_path}]
            )
            os.remove(temp_path)
            st.success(f"{update_id} updated successfully")
            st.rerun()
    else:
        st.info("No resumes available to update")
elif page == "All Resumes":
    st.title("All Resumes")
    if all_ids:
        for rid in sorted(all_ids):
            st.write("Resume name:", rid)
    else:
        st.info("No resumes found")