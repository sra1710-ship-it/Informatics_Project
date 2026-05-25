import streamlit as st
import sqlite3

# Деректер базасын және кестелерді дайындау
def init_db():
    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, name TEXT, password TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS survey_results (student TEXT, answer TEXT)')
    
    # 20 оқушы тізімі
    students = [
        ("user1", "Жандәулет", "123"), ("user2", "Аружан", "123"), ("user3", "Әбубәкір", "123"),
        ("user4", "Батырхан", "123"), ("user5", "Асылхан", "123"), ("user6", "Әмина", "123"),
        ("user7", "Аяна", "123"), ("user8", "Айару", "123"), ("user9", "Махамбет", "123"),
        ("user10", "Нұрхан", "123"), ("user11", "Батыр", "123"), ("user12", "Оқушы 12", "123"),
        ("user13", "Оқушы 13", "123"), ("user14", "Оқушы 14", "123"), ("user15", "Оқушы 15", "123"),
        ("user16", "Оқушы 16", "123"), ("user17", "Оқушы 17", "123"), ("user18", "Оқушы 18", "123"),
        ("user19", "Оқушы 19", "123"), ("user20", "Оқушы 20", "123")
    ]
    for s in students:
        cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", s)
    conn.commit()
    conn.close()

init_db()

# Негізгі бет
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
    else: 
        st.error("Логин немесе пароль қате!")
    conn.close()

# Сауалнама беті
if st.session_state.get('logged_in'):
    st.write(f"Қош келдіңіз, {st.session_state.user}!")
    with st.form("survey_form"):
        st.subheader("Оқушы сауалнамасы")
        q1 = st.radio("1. Сабаққа қызығушылығыңыз:", ["Жоғары", "Орташа", "Төмен"])
        q2 = st.radio("2. Тақырыпты түсіну деңгейі:", ["Толық түсіндім", "Орташа", "Қиын болды"])
        q3 = st.text_area("3. Не түсініксіз болды?")
        q4 = st.radio("4. Тапсырмалардың қиындығы:", ["Оңай", "Қалыпты", "Қиын"])
        q5 = st.radio("5. Мұғалімнің түсіндіруі:", ["Түсінікті", "Түсініксіз"])
        
        if st.form_submit_button("Жіберу"):
            conn = sqlite3.connect("school_data.db")
            cur = conn.cursor()
            ans = f"Қызығу:{q1}; Түсіну:{q2}; Сұрақ:{q3}; Қиындық:{q4}; Түсіндіру:{q5}"
            cur.execute("INSERT INTO survey_results VALUES (?,?)", (st.session_state.user, ans))
            conn.commit()
            conn.close()
            st.success("Жауабыңыз жіберілді!")
