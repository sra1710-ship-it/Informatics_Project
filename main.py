# Басты бет және беттерді басқару
    if st.session_state.page == "Басты бет":
        st.header("Платформаға қош келдіңіз!")
        
    elif st.session_state.page == "Сауалнама":
        st.header("📝 Сауалнама")
        # Сұрақтарды осы жерге қойыңыз
        q1 = st.radio("1. Сабақ қызықты ма?", ["Иә", "Жоқ"])
        if st.button("Жіберу"):
            cur.execute("INSERT INTO survey_results VALUES (?,?)", (st.session_state.user, q1))
            conn.commit()
            st.success("Сақталды!")
            
    elif st.session_state.page == "Тапсырма":
        st.header("🎮 Тапсырма")
        
    elif st.session_state.page == "Мониторинг":
        st.header("📊 Мониторинг")
        
    else:
        st.write("Бет табылмады")
