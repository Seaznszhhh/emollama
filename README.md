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
2. 基于 RAG 的心理健康对话治疗。
3. 患者档案的存取。

<div align="center">
<img src="figure\intro.png" width="700"/>
  <div>&nbsp;</div>
  <div align="center">
  </div>
</div>

---

# quick start

本项目使用[Ollama](https://ollama.com/)部署本地大模型，可实现多种最新大模型低精度的一键部署，妈妈再也不用担心显存不够用了。[Ollama](https://ollama.com/)目前支持多种操作系统，由于笔者是在 Linux 服务器上部署，所以一下简单展示在 Linux 环境怎么使用 Emollama。

<div align="center">
<img src="figure\ollama.png" width="400"/>
  <div>&nbsp;</div>
  <div align="center">
  </div>
</div>

## clone 本项目

```shell
git clone https://github.com/Seaznszhhh/emollama.git
```

打开你的工作目录后运行克隆。

## 安装 Ollama

```shell
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama run llama
```

如果成功运行大模型，你已经成功部署了 Ollama。本项目使用的 qwen:14b-chat 和 llava，需要 pull 一下模型。

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

## 在本地运行 streamlit

以 autodl 为例，在本地的 cmd 中运行下面的代码

```shell
ssh -CNg -L 8501:127.0.0.1:8501 root@connect.bjb1.seetacloud.com -p 14973
```

8501 要换成 streamlit run 后出现的地址所给的，14973 换成你的服务器实例给的端口。运行后出现输入密码，粘贴服务器实例密码，注意这里不会显示密码，直接按回车。然后打开本地浏览器输入 127.0.0.1:8501 就可以打开在远程服务器跑的 streamlit 页面了。

## 使用 Llama-factory 对模型进行 fine-tune

原作者：@article{zheng2024llamafactory,
title={LlamaFactory: Unified Efficient Fine-Tuning of 100+ Language Models},
author={Yaowei Zheng and Richong Zhang and Junhao Zhang and Yanhan Ye and Zheyan Luo and Yongqiang Ma},
journal={arXiv preprint arXiv:2403.13372},
year={2024},
url={http://arxiv.org/abs/2403.13372}
}

# 安装需要的包

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

# 运行

```shell
CUDA_VISIBLE_DEVICES=0 python src/train_web.py
```

# emollama 使用实例

待续。。。。
