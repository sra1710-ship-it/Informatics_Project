import streamlit as st
import sqlite3

st.title("💻 Informatics Platform")
username = st.text_input("Логин")
password = st.text_input("Пароль", type="password")

if st.button("Кіру"):
    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    user = cur.execute("SELECT name FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user[0]
        st.rerun()
    else: st.error("Қате!")

if st.session_state.get('logged_in'):
    st.write(f"Қош келдіңіз, {st.session_state.user}!")
    with st.form("survey_form"):
        q1 = st.radio("1. Сабаққа қызығушылығыңыз:", ["Жоғары", "Орташа", "Төмен"])
        q2 = st.radio("2. Тақырыпты түсіну деңгейі:", ["Толық түсіндім", "Орташа", "Қиын болды"])
        q3 = st.text_area("3. Не түсініксіз болды?")
        q4 = st.radio("4. Тапсырмалардың қиындығы:", ["Оңай", "Қалыпты", "Қиын"])
        q5 = st.radio("5. Мұғалімнің түсіндіруі:", ["Түсінікті", "Түсініксіз"])
        
        if st.form_submit_button("Жіберу"):
            conn = sqlite3.connect("school_data.db")
            cur = conn.cursor()
            ans = f"Қызығу: {q1}; Түсіну: {q2}; Сұрақ: {q3}; Қиындық: {q4}; Түсіндіру: {q5}"
            cur.execute("INSERT INTO survey_results VALUES (?,?)", (st.session_state.user, ans))
            conn.commit()
            st.success("Жауабыңыз жіберілді!")
