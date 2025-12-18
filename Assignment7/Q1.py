import streamlit as st
from langchain.chat_models import init_chat_model
import os
import pandas as pd
from dotenv import load_dotenv
from pandasql import sqldf
load_dotenv()
st.set_page_config(page_title="CSV Explorer", layout="wide")
st.title("CSV Explorer")
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])
if csv_file:
    df = pd.read_csv(csv_file)
    st.subheader("CSV Schema")
    st.write(df.dtypes)
    question = st.text_input("Ask anything about this CSV")
    if question:
        llm_input = f"""
        You are an expert SQL developer.
        Table Name : df
        Table Schema : {df.dtypes}
        Question : {question}
        Instruction :
        - Generate ONLY a valid SQLite SQL query
        - Do NOT use markdown or code blocks
        - Do NOT explain anything
        """
        query = llm.invoke(llm_input).content.strip()
        query = query.replace("```sql", "").replace("```", "").strip()
        st.subheader("Generated SQL Query")
        st.code(query, language="sql")
        try:
            result = sqldf(query, {"df": df})
            st.subheader("Query Result")
            st.dataframe(result)
            explain_prompt = f"""
            Explain the following result in simple English.
            Question : {question}
            Result : {result.head().to_string(index=False)}
            """
            explanation = llm.invoke(explain_prompt).content.strip()
            st.subheader("Explanation")
            st.write(explanation)
        except Exception as e:
            st.error(f"SQL Error: {e}")