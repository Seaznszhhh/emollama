# from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate

from langchain_core.pydantic_v1 import BaseModel, Field
#from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
#import streamlit as st
#import time
import gradio as gr

llm = Ollama(model="qwen:14b")

class score_mark(BaseModel):
    score: int = Field(description="Depression score")
    reason: str = Field(description="Reasons for obtaining the score")
parser = JsonOutputParser(pydantic_object=score_mark)
    
from langchain.schema.runnable import RunnableLambda
from operator import itemgetter
import pandas as pd
#from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
#from langchain.schema.runnable import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

def print_question(_dict):
    df = pd.read_excel(_dict["filename"])
    
    column_contents = df['question'].tolist()
    
    # 返回第n行的内容
    if _dict["n"] <= len(column_contents):
        return column_contents[_dict["n"] - 1]  # 索引从0开始，因此需要减1
    else:
        return "调取问卷失败"


prompt_1 = ChatPromptTemplate.from_template("""
        You are a doctor of postpartum depression, 
        please ask me question based on the following questionnaire question, 
        you should turn the statement into one question.
        Please use Chinese as your language.
        statement:{question}                                  
        """)

prompt_2 = PromptTemplate(
        input_variables=['question','answer'],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    
        template = """
        你现在是一名产后抑郁医生，你已经根据抑郁量表中问题向用户进行提问，现在希望你根据用户的主观回答进行评分。
        0分表示抑郁程度比较低，3分表示抑郁程度比较高。
        请你以json格式返回0、1、2、3中的数字以及原因。
           

        result format:{format_instructions}
        Please use Chinese as your language.
        Now begin!
        question posed before:{question}
        answer from the puerpera :{answer}        
        
        """,
        validate_template = False
        
        )

prompt_3 = ChatPromptTemplate.from_template("""
        You are now a postpartum depression doctor, you have asked the user questions based on the depression scale, and the user has answered your questions.
        According to your questions and the user's answers, please properly soothe the mood of the pregnant woman and make her more positive.
        limit: under 50 words
        limit: don't ask questions
        Please use Chinese as your language.
        Now begin!
        question posed before:{question}
        answer from the puerpera :{answer}  
                                            """)

prompt_4 = ChatPromptTemplate.from_template("""
        firstly,you are a postpartum depression doctor.Please use Chinese as your language.
        the mother completed the depression scale survey in the form of a conversation with you, 
        here is your chat history and corresponding scores. {chat_history}
        the score value of each question is 0~3 points, there are 10 questions.
        
        secondly,This is the final scores: {sum}

        Please make some suggestions based on the above information.please properly soothe the mood of the pregnant woman and make her more positive.
                                            """)

        

sum = 0
n = 0
answer = []
chat_history = {}
question = []

def QA(answer):   
    global sum 
    global n
    global chat_history     
    global question
    
    if n == 0:
        n +=1
        return "现在我们开始心理健康测试吧。请你尽可能详细地回答我的问题。你不要觉得压力，我会通过人工智能帮助诊断。"
    elif n == 1:
        
        print(f"\n------------------------------  QUESTION {n}   ----------------------------\n")
        chain1 = {
            "question":{"filename":itemgetter("file"),"n":itemgetter("number")} | RunnableLambda(print_question)
            # "length":{"text":itemgetter("abc")} | RunnableLambda(tellme)
                
        } | prompt_1 | llm 
        question = chain1.invoke({"file":"./knowledge/question.xlsx","number":n})
        print(f"QUESTION={question}")
        result = question
        n +=1
        return result
    elif 1 <= n <= 10:    
        chain2 = prompt_2 | llm | parser
        print(chain2)
        while True:
            try:
                result2 = chain2.invoke({"question":question,"answer":answer})
            except:
                print("++++++++++++++++++++++++++++++此处报错重新执行+++++++++++++++++++++++++++")
                continue
            else:
                break
        print(result2)
        score = result2['score']
        print(score)
        sum = sum + score
        print(f"\n----------  SCORE {n-1}  ------------\n")
        print(result2)


        chain3 = prompt_3 | llm
        print(f"\n---------  SUGGESTION {n-1}  ----------\n")
        suggestion = chain3.invoke({"question":question,"answer":answer})
        print(suggestion)

        question = []
        print(f"\n------------------------------  QUESTION {n}   ----------------------------\n")
        print(itemgetter("file"))
        print(itemgetter("number"))
        chain1 = {
            "question":{"filename":itemgetter("file"),"n":itemgetter("number")} | RunnableLambda(print_question)
            # "length":{"text":itemgetter("abc")} | RunnableLambda(tellme)
                
        } | prompt_1 | llm 
        question = chain1.invoke({"file":"./knowledge/question.xlsx","number":n})
    
        chat_history[f"Round{n}"] = {"Q":question,"A":answer,"score":score}
            
        
        result =  "\n" + suggestion +  "\n" + question
        n +=1
        return result
    elif n == 11:    
        chain2 = prompt_2 | llm | parser
        print(chain2)
        while True:
            try:
                result2 = chain2.invoke({"question":question,"answer":answer})
            except:
                print("++++++++++++++++++++++++++++++此处报错重新执行+++++++++++++++++++++++++++")
                continue
            else:
                break
        print(result2)
        score = result2['score']
        print(score)
        sum = sum + score
        print(f"\n----------  SCORE {n-1}  ------------\n")
        print(result2)


        chain3 = prompt_3 | llm
        print(f"\n---------  SUGGESTION {n-1}  ----------\n")
        suggestion = chain3.invoke({"question":question,"answer":answer})
        print(suggestion)

       
            
  
        result =  "\n" + suggestion +  "\n" + "提问已结束，下面开始总结。"
        n +=1
        return result
    elif n == 12:
        chain4 = prompt_4 | llm
        result4 = chain4.invoke({"chat_history": chat_history,"sum":sum})  
        print(f"\n------------------------------  FINAL   ----------------------------\n") 
        print("\n final score : ",sum)
        print("\n",result4)
        result = result4
        n +=1
        return result
    else:
        return "问卷到此结束"


if __name__ == "__main__":  
    demo_chat = gr.ChatInterface(fn=QA)
    demo_chat.launch() 
        
        
        
    
    
    
    
    
    
    
    
    
    
    


