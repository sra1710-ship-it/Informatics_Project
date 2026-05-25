import streamlit as st
import sqlite3
import pandas as pd

st.title("👩‍🏫 Мұғалім журналы")
conn = sqlite3.connect("school_data.db")
try:
    results = pd.read_sql("SELECT * FROM survey_results", conn)
    st.table(results)
except:
    st.write("Әлі нәтижелер жоқ.")

if st.button("Жаңарту"):
    st.rerun()
