import streamlit as st
import sqlite3

def init_db():
    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, name TEXT, password TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS survey_results (student TEXT, answer TEXT)')
    
    # 20 оқушыны қосу
    students = [("user1", "Жандәулет", "123"), ("user2", "Аружан", "123")]
    for s in students:
        cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", s)
    conn.commit()
    conn.close()

init_db()

st.title("💻 Informatics Platform")

username = st.text_input("Логин")
password = st.text_input("Пароль", type="password")

if st.button("Кіру"):
    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    # Базада не бар екенін тексеру үшін
    user = cur.execute("SELECT name FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user[0]
        st.rerun()
    else:
        # Егер қате болса, базада тіпті оқушылар бар ма, соны тексереміз
        count = cur.execute("SELECT count(*) FROM users").fetchone()[0]
        st.error(f"Қате! Базада барлығы {count} оқушы бар. Логин/парольді тексеріңіз.")
    conn.close()

if st.session_state.get('logged_in'):
    st.success(f"Қош келдіңіз, {st.session_state.user}!")
    # Сауалнама формасы... (алдыңғы кодтағыдай)
