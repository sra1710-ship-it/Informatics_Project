import streamlit as st
import sqlite3

# Базаны қосу
conn = sqlite3.connect("school_data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, name TEXT, class TEXT, password TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS survey_results (student TEXT, answer TEXT)')

# Сессияны бастау
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Басты бет"

def login_func():
    user = cur.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (st.session_state.username, st.session_state.password)).fetchone()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user[1]
    else: st.error("Қате!")

if not st.session_state.logged_in:
    st.text_input("Логин", key="username")
    st.text_input("Пароль", type="password", key="password")
    if st.button("Кіру"): login_func()
else:
    st.sidebar.title(f"Сәлем, {st.session_state.user}!")
    if st.sidebar.button("🏠 Басты бет"): st.session_state.page = "Басты бет"
    if st.sidebar.button("📝 Сауалнама"): st.session_state.page = "Сауалнама"
    if st.sidebar.button("🚪 Шығу"): st.session_state.logged_in = False; st.rerun()

    if st.session_state.page == "Басты бет":
        st.header("Платформаға қош келдіңіз!")
    elif st.session_state.page == "Сауалнама":
        st.header("📝 Сауалнама")
        # Барлық сұрақтарды осы жерге қосамыз
        with st.form("survey_form"):
            q1 = st.radio("1. Қызығушылығыңыз қалай өзгерді?", ["Артты", "Ішінара жоғарылады", "Өзгеріс жоқ", "Кері әсер"])
            q2 = st.radio("2. Күрделі тақырыптарды түсінуге әсері:", ["Терең түсіну", "Жеңілдетеді", "Қиындық тудырады", "Әсер етпейді"])
            q3 = st.text_input("3. Тапсырма форматы туралы пікіріңіз:")
            q4 = st.radio("4. Мотивациялық рөлі:", ["Жоғары", "Орташа", "Төмен", "Әсері жоқ"])
            q5 = st.radio("5. Терминдерді есте сақтау тиімділігі:", ["Жоғары", "Орташа", "Төмен"])
            q6 = st.text_area("6. Инновациялық ойын ұсынысыңыз:")
            # ... осылай барлық сұрақты қосып шығыңыз ...
            
            submitted = st.form_submit_button("Жіберу")
            if submitted:
                ans = f"1:{q1}; 2:{q2}; 3:{q3}; 4:{q4}; 5:{q5}; 6:{q6}"
                cur.execute("INSERT INTO survey_results VALUES (?,?)", (st.session_state.user, ans))
                conn.commit()
                st.success("Сауалнамаңыз сәтті сақталды!")
