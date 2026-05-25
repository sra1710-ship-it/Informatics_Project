import streamlit as st
import sqlite3
import streamlit.components.v1 as components

# --- ДЕРЕКҚОР ЖӘНЕ ТІЗІМ ---
conn = sqlite3.connect("school_data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, name TEXT, class TEXT, password TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS results (student TEXT, task TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS survey_results (student TEXT, answer TEXT)')

# 20 оқушыны базаға енгізу (болмаса)
students = [("5a_zhandaulet", "Жандәулет", "5-А", "1234"), ("5ae_aminah", "Амина", "5-Ә", "5678")] + \
           [(f"s{i}", f"Оқушы {i}", "5-А", "111") for i in range(3, 21)]
for s in students: cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?)", s)
conn.commit()

# --- СЕССИЯ ЖӘНЕ ЛОГИН ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Басты бет"

def login_func():
    user = cur.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (st.session_state.username, st.session_state.password)).fetchone()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user[1]
    else: st.error("Қате логин/пароль!")

# --- ИНТЕРФЕЙС ---
if not st.session_state.logged_in:
    st.title("💻 Informatics Platform")
    st.text_input("Логин", key="username")
    st.text_input("Пароль", type="password", key="password", on_change=login_func)
    if st.button("Кіру"): login_func()
else:
    st.sidebar.title(f"Сәлем, {st.session_state.user}!")
    # Навигация батырмалары
    if st.sidebar.button("🏠 Басты бет"): st.session_state.page = "Басты бет"
    if st.sidebar.button("📝 Сауалнама"): st.session_state.page = "Сауалнама"
    if st.sidebar.button("🎮 Тапсырма"): st.session_state.page = "Тапсырма"
    if st.sidebar.button("📊 Мониторинг"): st.session_state.page = "Мониторинг"
    if st.sidebar.button("🚪 Шығу"): st.session_state.logged_in = False; st.rerun()

    # Беттерді көрсету
    if st.session_state.page == "Басты бет":
        st.header("Платформаға қош келдіңіз!")
    elif st.session_state.page == "Сауалнама":
        st.header("📝 Сауалнама")
        ans = st.radio("Сабақ ұнай ма?", ["Иә", "Жоқ"])
        if st.button("Жіберу"):
            cur.execute("INSERT INTO survey_results VALUES (?,?)", (st.session_state.user, ans))
            conn.commit()
            st.success("Сақталды!")
    elif st.session_state.page == "Тапсырма":
        st.header("🎮 Тапсырма")
        components.iframe("https://learningapps.org/watch?v=pexample123", height=500)
        if st.button("Орындадым"):
            cur.execute("INSERT INTO results VALUES (?,?)", (st.session_state.user, "LearningApps"))
            conn.commit()
            st.success("Нәтиже сақталды!")
    elif st.session_state.page == "Мониторинг":
        st.header("📊 Мониторинг")
        st.table(cur.execute("SELECT * FROM results").fetchall())
        st.table(cur.execute("SELECT * FROM survey_results").fetchall())
