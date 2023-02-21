from datetime import *
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

datenow=datetime.now(tz=timezone(timedelta(hours=8)))
today = datenow.strftime('%Y-%m-%d')#今日日期字符串
weekd=datenow.weekday()#星期数


city = os.environ['CITY']

token_alapi=os.environ['TOKEN_ALAPI']#在alapi.cn自行注册得到的token
tp=randint(1,45)

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


className=("高等数学ⅠA","大学英语基础模块A","工程图学Ⅲ","思想道德与法治","计算思维与程序设计基础","军事理论","过程装备与控制工程专业导论课","艺术散步","体育Ⅰ","大学生职业发展与就业指导（上）")#9
classRoom=("1-404","1-406","6-204","6-301","6-304","7B-403","7B-407","7C-201","7C-203","7C-207","7C-403","操场","机房","7C-303","7C-301")#14
classTable=(((0,7),(-1,-1),(2,8),(-1,-1),(7,4),(-1,-1)) , ((1,6),(2,5),(3,1),(4,10),(-1,-1),(-1,-1)) , ((-1,-1),(0,7),(4,12),(-1,-1),(5,3),(5,3)) , ((3,0),(8,11),(0,8),(-1,-1),(-1,-1),(-1,-1)) , ((0,7),(2,7),(-1,-1),(-1,-1),(9,2),(9,2)) , ((-1,-1),(-1,-1),(-1,-1),(1,3),(-1,-1),(-1,-1)) , ((-1,-1),(-1,-1),(9,14),(9,14),(-1,-1),(-1,-1)))
sttime=(830,1025,1400,1555,1840,2020)
edtime=(1005,1200,1535,1730,2015,2105)

def table2str():
  tbstr=""
  lst=lstm=-1
  cfg=False
  for i in range(6):
    ntb=classTable[weekd][i]
    if ntb[0] != -1:
      if lst == ntb[0]:
        cfg=True
    
    if lst != -1 and not cfg:
      tmpstr="{}:{:0>2}-{}:{:0>2}".format(sttime[lstm]//100,sttime[lstm]%100,edtime[i-1]//100,edtime[i-1]%100)
      tbstr+="{:^18}\n{:^18}\n{:^18}\n".format(className[lst],classRoom[classTable[weekd][lstm][1]],tmpstr)
    if not cfg:
      lst=ntb[0]
      lstm=i
    cfg=False
  if lst != -1:
    tmpstr="{}:{:0>2}-{}:{:0>2}".format(sttime[lstm]//100,sttime[lstm]%100,edtime[5]//100,edtime[5]%100)
    tbstr+="{:^18}\n{:^18}\n{:^18}\n".format(className[lst],classRoom[classTable[weekd][lstm][1]],tmpstr)
  return tbstr




def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low']),math.floor(weather["high"]),weather["airQuality"]

def get_date():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days


def get_words():
  words = requests.get("https://v2.alapi.cn/api/mingyan?typeid={}&token={}".format(tp,token_alapi))
  if words.status_code != 200:
    return get_words()
  wd=words.json()['data']['content']
  au=words.json()['data']["author"]
  return wd+'-'*5+au

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)



client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temlow,temhigh,airq = get_weather()
data = {"weather":{"value":wea},"temlow":{"value":temlow},"temhigh":{"value":temhigh},"airq":{"value":airq},
        "date":{"value":get_date()},"words":{"value":get_words(), "color":get_random_color()},
        "class":{"value":table2str()}}
res = wm.send_template(user_id, template_id, data)
print(res)

