import streamlit as st
import sqlite3

# Деректер базасын қосу
conn = sqlite3.connect("school_data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, name TEXT, password TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS survey_results (student TEXT, answer TEXT)')

# 20 оқушыны базаға енгізу
students = [
    ("user1", "Оқушы 1", "123"), ("user2", "Оқушы 2", "123"), ("user3", "Оқушы 3", "123"),
    ("user4", "Оқушы 4", "123"), ("user5", "Оқушы 5", "123"), ("user6", "Оқушы 6", "123"),
    ("user7", "Оқушы 7", "123"), ("user8", "Оқушы 8", "123"), ("user9", "Оқушы 9", "123"),
    ("user10", "Оқушы 10", "123"), ("user11", "Оқушы 11", "123"), ("user12", "Оқушы 12", "123"),
    ("user13", "Оқушы 13", "123"), ("user14", "Оқушы 14", "123"), ("user15", "Оқушы 15", "123"),
    ("user16", "Оқушы 16", "123"), ("user17", "Оқушы 17", "123"), ("user18", "Оқушы 18", "123"),
    ("user19", "Оқушы 19", "123"), ("user20", "Оқушы 20", "123")
]
for s in students:
    cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", s)
conn.commit()

# Сессияны басқару
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

def login_func():
    user = cur.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (st.session_state.username, st.session_state.password)).fetchone()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user[1]
    else: st.error("Логин немесе пароль қате!")

# Интерфейс
if not st.session_state.logged_in:
    st.title("💻 Informatics Platform")
    st.text_input("Логин", key="username")
    st.text_input("Пароль", type="password", key="password")
    if st.button("Кіру"): login_func()
else:
    st.sidebar.title(f"Сәлем, {st.session_state.user}!")
    if st.sidebar.button("🚪 Шығу"): st.session_state.logged_in = False; st.rerun()

    st.header("📝 Сауалнама")
    with st.form("survey_form"):
        q1 = st.radio("1. Сабаққа қызығушылығыңыз:", ["Жоғары", "Орташа", "Төмен"])
        q2 = st.radio("2. Тақырыпты түсіну деңгейі:", ["Толық түсіндім", "Орташа", "Қиын болды"])
        q3 = st.text_area("3. Не түсініксіз болды?")
        q4 = st.radio("4. Тапсырмалардың қиындығы:", ["Оңай", "Қалыпты", "Қиын"])
        q5 = st.radio("5. Мұғалімнің түсіндіруі:", ["Түсінікті", "Түсініксіз"])
        
        submitted = st.form_submit_button("Жіберу")
        if submitted:
            ans = f"1:{q1}; 2:{q2}; 3:{q3}; 4:{q4}; 5:{q5}"
            cur.execute("INSERT INTO survey_results VALUES (?,?)", (st.session_state.user, ans))
            conn.commit()
            st.success("Жауабыңыз сақталды!")
