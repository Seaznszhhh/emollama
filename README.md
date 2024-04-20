# 🤖Emollama 心理健康诊疗大模型

<div align="center">
<img src="figure\Emollama.png" width="400"/>
  <div>&nbsp;</div>
  <div align="center">
  </div>
</div>

---

# 简介
本项目为基于[Ollama](https://ollama.com/)进行本地大模型部署、[langchain](https://www.langchain.com/)开发，以及[streamlit](https://streamlit.io/)制作前端的心理抑郁诊断治疗大模型。包含以下三个主要功能。
1. 基于大模型沟通的智能心理健康诊断。
2. 基于RAG的心理健康对话治疗。
3. 患者档案的存取。

<div align="center">
<img src="figure\intro.png" width="700"/>
  <div>&nbsp;</div>
  <div align="center">
  </div>
</div>

---

# quick start

本项目使用[Ollama](https://ollama.com/)部署本地大模型，可实现多种最新大模型低精度的一键部署，妈妈再也不用担心显存不够用了。[Ollama](https://ollama.com/)目前支持多种操作系统，由于笔者是在Linux服务器上部署，所以一下简单展示在Linux环境怎么使用Emollama。

<div align="center">
<img src="figure\ollama.png" width="400"/>
  <div>&nbsp;</div>
  <div align="center">
  </div>
</div>

## clone本项目
```shell 
git clone https://github.com/Seaznszhhh/emollama.git
```
打开你的工作目录后运行克隆。

## 安装Ollama
```shell 
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama run llama 
```
如果成功运行大模型，你已经成功部署了Ollama。本项目使用的qwen:14b-chat和llava，需要pull一下模型。
```shell 
ollama pull qwen:14b-chat
ollama pull llava
```

## 安装环境
```shell 
cd emollama
pip install -r requirements.txt
```

## 运行
```shell 
streamlit run 主页面.py
```
由于是在服务器的端口并不是在本机，所以此时出现的地址是打不开的，还需要进行一下的步骤。

## 在本地运行streamlit
以autodl为例，在本地的cmd中运行下面的代码
```shell 
ssh -CNg -L 8501:127.0.0.1:8501 root@connect.bjb1.seetacloud.com -p 14973
```
8501要换成streamlit run 后出现的地址所给的，14973换成你的服务器实例给的端口。运行后出现输入密码，粘贴服务器实例密码，注意这里不会显示密码，直接按回车。然后打开本地浏览器输入127.0.0.1:8501就可以打开在远程服务器跑的streamlit页面了。

# emollama 使用实例
待续。。。。