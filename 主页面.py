import streamlit as st
from langchain_community.llms import Ollama
import time
import sqlite3
from page.page2 import page2
from page.page3 import page3
from page.page4 import page4

def page1(c,conn,user_name):
    st.title(f"🤩Emollama")
    # user_name = st.text_input("请输入您的姓名")
    user_age = st.number_input("请输入您的年龄", min_value=0, max_value=150)
    user_email = st.text_input("请输入您的电子邮箱")

    if st.button("🫰开启智能抑郁量表测试"):
        st.session_state['page'] = 'page4'
        time.sleep(1)
        st.experimental_rerun()
    
    if st.button("🫰开启心理治疗"):
        st.session_state.messages = []
        # 检查用户是否已经存在
        c.execute("SELECT id FROM users WHERE name=? AND age=? AND email=?", (user_name, user_age, user_email))
        existing_user = c.fetchone()

        if existing_user:
            st.write("# 欢迎回来！")
            st.session_state['page'] = 'page2'
            time.sleep(1)
            st.experimental_rerun()
            
        else:
            # 如果用户不存在，则插入新用户信息并获取用户ID
            c.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (user_name, user_age, user_email))
            conn.commit()
            st.write("# 欢迎新用户！")
            st.session_state['page'] = 'page2'
            time.sleep(1)
            st.experimental_rerun()


with sqlite3.connect('archive1.db') as conn:
    c = conn.cursor()
# 创建用户信息和聊天记录表
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    email TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS chats (
                    user_name TEXT,
                    message TEXT,
                    response TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    user_name = st.text_input("请输入您的姓名")
    if 'page' not in st.session_state:
        st.session_state['page'] = 'page1'
    if st.session_state['page'] == 'page1':
        page1(c,conn,user_name)
    elif st.session_state['page'] == 'page2':
        page2(c,conn,user_name)
    elif st.session_state['page'] == 'page3':
        page3(c,conn)
    elif st.session_state['page'] == 'page4':
        page4()
