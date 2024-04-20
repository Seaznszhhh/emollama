from langchain_community.llms import Ollama
import streamlit as st
from IPython.display import HTML, display
from io import BytesIO
from PIL import Image
import numpy as np
import base64
from generate_audio_tool import audiotool
import os

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
#from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

def page2(c,conn,user_name):
    def convert_to_base64(pil_image):
        """
        Convert PIL images to Base64 encoded strings

        """
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")  # You can change the format if needed
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    def plt_img_base64(img_base64):
        """
        Display base64 encoded string as image
        """
        image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'
        display(HTML(image_html))

    def generate_img_caption(img_file_buffer):
            print("--------------------开始生成图像理解---------------------")
            img = Image.open(img_file_buffer)
            img_array = np.array(img)
            st.image(img)
            pil_image = Image.fromarray(img_array)
            image_b64 = convert_to_base64(pil_image)
            plt_img_base64(image_b64)
            llm_with_image_context = llm.bind(images=[image_b64])
            return llm_with_image_context.invoke("用简短的语言描述图片中人物的心情")
        
    st.markdown("# 🦜🔗心理健康治疗机器人")
    model_list = ["qwen:14b-chat", "llava:7b"]
    object_list = ["孕期","中小学生","老年人"]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title(f"🤩Emollama")
    with st.sidebar:
        if st.button("返回"):
            st.session_state['page'] = 'page1'
            st.experimental_rerun()
        if st.button("查看存档"):
            st.session_state['page'] = 'page3'
            st.experimental_rerun()
        if st.button("🧸心理健康诊断"):
            st.session_state['page'] = 'page4'
            st.experimental_rerun()
        st.subheader("🚀Settings")

        #选择大模型
        llm_option = st.selectbox(
            '选择你想用的大模型🧑🏼‍💻',
            model_list)
        st.write('你选择了:', llm_option)

        #选择对象
        object_option = st.selectbox(
        '选择适用人群🙋🏼‍♀️',
        object_list)
        st.write('你选择了:', object_option)

        #上传图片
        img_file_buffer = st.file_uploader("上传图片", accept_multiple_files=False)
        if img_file_buffer is not None:
            llm = Ollama(model="llava:7b")
            img_describe = generate_img_caption(img_file_buffer=img_file_buffer)
            st.markdown(img_describe)

        #连接摄像头
        picture = st.camera_input("Take a picture")
        if picture is not None:
            llm = Ollama(model="llava:7b")
            img_describe = generate_img_caption(img_file_buffer=picture)
            st.markdown(img_describe)

    class RAG:
        def __init__(self, img_describe, llm, age="孕期", ):
            self.llm = llm
            self.img_describe=img_describe
            self.age = age
            embeddings = OllamaEmbeddings()
            #def load_text(self):
            if self.age =="中小学生":
                loader = TextLoader("./knowledge/01student.txt", encoding = "utf-8")
                persist_directory = './data_base/vector_db_for_student/chroma'  
            elif self.age =="孕期":
                loader = TextLoader("./knowledge/02pregnent.txt", encoding = "utf-8")
                persist_directory = './data_base/vector_db_for_pregent/chroma'  
            elif self.age =="老年人":
                loader = TextLoader("./knowledge/03aged.txt", encoding = "utf-8") 
                persist_directory = './data_base/vector_db_for_aged/chroma'  
            #没有数据库时才进行 提高运行效率  
            if not os.path.exists(persist_directory):
                print("--------------------正在生成新数据库---------------------")
                documents = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
                split_docs = text_splitter.split_documents(documents)
                self.db = Chroma.from_documents(documents=split_docs,embedding=embeddings,persist_directory=persist_directory)
                # 将加载的向量数据库持久化到磁盘上
                self.db.persist()
            #有数据库直接载入
            else:
                # 加载数据库
                print("--------------------正在载入已有数据库---------------------")
                self.db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        def QA(self,query,history=[]):
            print("--------------------开始检索生成---------------------")
            qa = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type='stuff',
                retriever=self.db.as_retriever(),
                verbose=True)
            prompt = f"""
            你是一个{self.age}心理健康聊天机器人，你在面对一个可能有心理问题的病人，这是他的情绪信息{img_describe}，回答他的问题{query}，语气要很温柔很温柔
            """
            answer=(qa(prompt)["result"])
            print(answer)
            return(answer)        

    llm = Ollama(model=llm_option)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("🫰说点什么吧"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            my_RAG=RAG(llm=llm, age=object_option, img_describe=img_describe )
            response = my_RAG.QA(prompt)
            c.execute("INSERT INTO chats (user_name, message, response) VALUES (?, ?, ?)", (user_name,prompt,response))
            audiotool(response)
            st.audio("./audio/1.mp3", format="audio/mpeg")
            st.markdown(response)
        conn.commit()
        st.session_state.messages.append({"role": "assistant", "content": response})


