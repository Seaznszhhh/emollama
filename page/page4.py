#from langchain_community.llms import Ollama
import streamlit as st
from generate_audio_tool import audiotool
from emollama_exam_gradio import QA

def page4():
    st.markdown("# 🧸心理健康诊断")
    with st.sidebar:
        if st.button("返回"):
            st.session_state['page'] = 'page1'
            st.experimental_rerun()
        if st.button("查看存档"):
            st.session_state['page'] = 'page3'
            st.experimental_rerun()
        if st.button("🦜🔗心理健康治疗机器人"):
            st.session_state['page'] = 'page2'
            st.experimental_rerun()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title(f"🤩Emollama")      

    #llm = Ollama(model=llm_option)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("🫰输入任意信息开始对话"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = QA(prompt)
            audiotool(response)
            st.audio("./audio/1.mp3", format="audio/mpeg")
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


