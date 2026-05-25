import streamlit as st
import sqlite3

# 1. Базаны қосу
conn = sqlite3.connect("school_data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, name TEXT, class TEXT, password TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS survey_results (student TEXT, answer TEXT)')

# 2. Сессияны бастау
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Басты бет"

# 3. Логин функциясы
def login_func():
    user = cur.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (st.session_state.username, st.session_state.password)).fetchone()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user[1]
    else: st.error("Қате логин/пароль!")

# 4. Негізгі интерфейс
if not st.session_state.logged_in:
    st.title("💻 Informatics Platform")
    st.text_input("Логин", key="username")
    st.text_input("Пароль", type="password", key="password")
    if st.button("Кіру"): login_func()
else:
    # МҰҒАЛІМ/ОҚУШЫ МӘЗІРІ
    st.sidebar.title(f"Сәлем, {st.session_state.user}!")
    if st.sidebar.button("🏠 Басты бет"): st.session_state.page = "Басты бет"
    if st.sidebar.button("📝 Сауалнама"): st.session_state.page = "Сауалнама"
    if st.sidebar.button("🎮 Тапсырма"): st.session_state.page = "Тапсырма"
    if st.sidebar.button("📊 Мониторинг"): st.session_state.page = "Мониторинг"
    if st.sidebar.button("🚪 Шығу"): st.session_state.logged_in = False; st.rerun()

    # БЕТТЕРДІҢ МАЗМҰНЫ
    if st.session_state.page == "Басты бет":
        st.header("Платформаға қош келдіңіз!")
        
    elif st.session_state.page == "Сауалнама":
        st.header("📝 Сауалнама")
        q1 = st.radio("1. Сабақ қызықты ма?", ["Иә", "Жоқ"])
        if st.button("Жіберу"):
            cur.execute("INSERT INTO survey_results VALUES (?,?)", (st.session_state.user, q1))
            conn.commit()
            st.success("Сақталды!")
            
    elif st.session_state.page == "Тапсырма":
        st.header("🎮 Тапсырма")
        
    elif st.session_state.page == "Мониторинг":
        st.header("📊 Мониторинг")
