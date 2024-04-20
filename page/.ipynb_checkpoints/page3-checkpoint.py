import streamlit as st


def page3(c,conn):
    st.markdown("## 📑存档记录")
    c.execute("SELECT name, message, response, timestamp FROM users INNER JOIN chats ON users.name = chats.user_name")
    archive = c.fetchall()
    conn.commit()
    for entry in archive:
         st.write(f"姓名: {entry[0]}, 患者消息: {entry[1]}, Ollama回答：{entry[2]}, 时间: {entry[3]}")

    with st.sidebar:
        if st.button("返回"):
            st.session_state['page'] = 'page2'
            st.experimental_rerun()