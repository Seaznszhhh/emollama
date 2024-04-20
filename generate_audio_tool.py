import os

def audiotool(str):
    print("--------------------开始生成音频---------------------")
    for object in ["\t", "\n", "\r"," ", "*","-","+","|","'",";","!",":","#","%","&","~","=","^",".",",","<",">"]:
        str = str.replace(object, "。")
    print(str)
    location = os.getcwd()
    print(location)
    strings = ["edge-tts --text", str, "--write-media", "./audio/1.mp3", "--voice","zh-CN-XiaoxiaoNeural"]
    cmd = " ".join(strings)
    os.system(cmd)

if __name__ == "__main__":
    audiotool("我有一只小毛驴我从来都不骑，有一天我心血来潮骑着它去赶集")