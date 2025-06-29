import time,datetime,json,os,sys
import platform

from utils.logger_settings import api_logger
from urllib.parse import urlparse
import socket
import struct
import subprocess
# import torch
import shutil
import string
import random
import requests

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def split(todo_text):
    splits = {"，", "。", "？", "！", ",", ".",
              "?", "!", "~", ":", "：", "—", "…", }
    todo_text = todo_text.replace("……", "。").replace("——", "，")
    if todo_text[-1] not in splits:
        todo_text += "。"
    i_split_head = i_split_tail = 0
    len_text = len(todo_text)
    todo_texts = []
    while 1:
        if i_split_head >= len_text:
            break  # 结尾一定有标点，所以直接跳出即可，最后一段在上次已加入
        if todo_text[i_split_head] in splits:
            i_split_head += 1
            todo_texts.append(todo_text[i_split_tail:i_split_head])
            i_split_tail = i_split_head
        else:
            i_split_head += 1
    return todo_texts

# 常用工具
class Util:

  # 执行Linux命令
  def Exec(cmd: str):
    res = os.popen(cmd)
    return res.readlines()

  # 格式化时间
  def Date(format: str='%Y-%m-%d %H:%M:%S', timestamp: float=None):
    t = time.localtime(timestamp)
    return time.strftime(format, t)


  # 时间戳
  def Time():
    return int(time.time())

  # String To Timestamp
  def StrToTime(day: str=None, format: str='%Y-%m-%d %H:%M:%S'):
    tArr = time.strptime(day, format)
    t = time.mktime(tArr)
    return t if t>0 else 0

  # Timestamp To GmtIso8601
  def GmtISO8601(timestamp: int):
    t = time.localtime(timestamp)
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", t)

  # 去首尾空格
  def Trim(content, charlist: str = None):
    text = str(content)
    return text.strip(charlist)

  # String to List
  def Explode(delimiter: str, string: str):
    return string.split(delimiter)

  # List to String
  def Implode(glue: str, pieces: list):
    return glue.join(pieces)

  # Array to String
  def JsonEncode(data):
    try :
      return json.dumps(data)
    except Exception as e :
      return ''

  # String to Array
  def JsonDecode(data: str):
    try :
      return json.loads(data)
    except Exception as e :
      return []

  # 合并数组
  def ArrayMerge(*arrays: dict):
    res = {}
    for arr in arrays :
      for k,v in arr.items() : res[k] = v
    return res

  # Url to Array
  def UrlToArray(url: str):
    if not url : return {}
    arr = url.split('?')
    path = arr[1] if len(arr)>1 else arr[0]
    arr = path.split('&')
    param = {}
    for v in arr :
      tmp = v.split('=')
      param[tmp[0]] = tmp[1]
    return param
  
  def is_folder(path):
    if os.path.exists(path) and os.path.isdir(path):
        return True
    else:
        return False   


  def createFolder(path):
   if not Util.is_folder(path):
       os.makedirs(path)

  def clearDir(path):
   # 删除文件夹中的所有文件
   for root, dirs, files in os.walk(path):
       for file in files:
           os.remove(os.path.join(root, file))

  def clearFilesOrDirsExcept(filepath):
    # 删除文件夹中的所有文件
    dirpath = os.path.dirname(filepath)
    for root, dirs, files in os.walk(dirpath):
      for file in files:
          stepfilepath = os.path.join(root, file)
          if stepfilepath != filepath:
              os.remove(stepfilepath)
      for dir in dirs:
          # os.rmdir(os.path.join(root, dir))
          shutil.rmtree(os.path.join(root, dir), ignore_errors=True)

  def isStringInList(srcStr:str, inStrList):
      return any(srcStr in item for item in inStrList)
  
  def isMac():
    platform_ = platform.system()
    if platform_ == "Mac" or platform_ == "Darwin":
      return True
    
    return False

  def addHashTag(input=""):
    if len(input) == 0:
        return ""
    hashwords = ['eth', 'bitcoin', 'btc', 'genesis', 'ethereum', 'bnb', 'ada', 'cardano', 'dogecoin', 'doge', "litecoin", "ltc", "solana", "sol", "xrp", "xrp", "ripple", "shiba", "shiba-inu", "shib", "shibainu", "shibaswap", "bch", ]

    words = input.split()
    for word in words:
        if word[0] != '#':
            if word.lower() in hashwords:
                input = input.replace(" " + word, " #"+word)

    print(input)
    return input
  

  def sliceStringWithSentence(inStr, sentenceStep=4):
    inStr = inStr.strip("\n")
    inps = split(inStr)
    lenInps = len(inps)
    split_idx = list(range(0, lenInps, sentenceStep))
    split_idx[-1] = None
    if len(split_idx) > 1:
        opts = []
        for idx in range(len(split_idx) - 1):
            opts.append("".join(inps[split_idx[idx]: split_idx[idx + 1]]))
    else:
        opts = [inStr]
    # return "\n".join(opts)
    return "\n".join(opts)

  def format_timestamp(seconds: float, always_include_hours: bool = False):
      '''format timestamp to SRT format'''
      assert seconds >= 0, "non-negative timestamp expected"
      milliseconds = round(seconds * 1000.0)

      hours = milliseconds // 3_600_000
      milliseconds -= hours * 3_600_000

      minutes = milliseconds // 60_000
      milliseconds -= minutes * 60_000

      seconds = milliseconds // 1_000
      milliseconds -= seconds * 1_000

      hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
      return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
  

  # 最后一个字符是中文标点符号。？！
  def lastCharIsCnClosePunctuations(inSrt):
    cnPunctuations: str = ["。","？","！"]
    ret = False
    if len(inSrt) > 0:
      lastChar = inSrt[len(inSrt) - 1]
      for punctuation in cnPunctuations:
        if lastChar == punctuation:
           ret = True
           break

    return ret
  
  # 最后一个字符是中文标点符号.?!
  def lastCharIsEnClosePunctuations(inSrt):
    punctuations: str = [".","?","!"]
    ret = False
    if len(inSrt) > 0:
      lastChar = inSrt[len(inSrt) - 1]
      for punctuation in punctuations:
        if lastChar == punctuation:
           ret = True
           break

    return ret

  def log_subprocess_output(inStr):
    if len(inStr) > 0:
        inStr = inStr.decode(sys.stdout.encoding)
        logStrList = inStr.split('\n')
        for line in logStrList:
            api_logger.info(line)


  def getProxy():
    if platform.system() == "Linux":
        return "192.168.0.77:18808"
    else:
       return "127.0.0.1:10809"
     

    
  def getCurTimeStampStr():
    timestamp = int(datetime.datetime.now().timestamp())
    string_timestamp = str(timestamp)
    return string_timestamp
  
  def getTempMp4FilePath():
      saveVideoName = f"{Util.getCurTimeStampStr()}.mp4"
      videoPath = os.path.join("/tmp/", saveVideoName)
      return videoPath
  
  def is_loopback(host):
    loopback_checker = {
        socket.AF_INET: lambda x: struct.unpack('!I', socket.inet_aton(x))[0] >> (32-8) == 127,
        socket.AF_INET6: lambda x: x == '::1'
    }
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            r = socket.getaddrinfo(host, None, family, socket.SOCK_STREAM)
        except socket.gaierror:
            return False
        for family, _, _, _, sockaddr in r:
            if not loopback_checker[family](sockaddr[0]):
                return False
    return True
  
  # 显存，返回 M 兆
  def get_first_gpu_memory():
    if platform.system() == "Linux":
      command = "nvidia-smi --query-gpu=memory.free --format=csv"
      memory_free_info = subprocess.check_output(command.split()).decode('ascii').split('\n')[:-1][1:]
      memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
      if len(memory_free_values) > 0:
          return memory_free_values[0]
      else:
          return 0
    else:
       return 0

  # 显存数组，返回 M 兆
  def get_gpu_memory():
    if platform.system() == "Linux":
      command = "nvidia-smi --query-gpu=memory.free --format=csv"
      memory_free_info = subprocess.check_output(command.split()).decode('ascii').split('\n')[:-1][1:]
      memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
      return memory_free_values
    else:
      return 0
    

  def get_total_num_gpus():
    try:
        n = len(subprocess.check_output(['nvidia-smi','-L']).decode('utf-8').strip().split('\n'))
    except OSError:
        n = 0
    return n 

  
  def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
  

  def download_file(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

  def get_file_name_and_ext(file_path):
    # 获取文件名（含后缀）
    file_name_with_ext = os.path.basename(file_path)
    # 分离文件名和后缀
    file_name, file_ext = os.path.splitext(file_name_with_ext)
    
    return file_name, file_ext