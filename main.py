import requests
from datauri import DataURI
import os
import random
import asyncio
import time
import threading

listdir = os.listdir('avatar')
image = 'avatar/' + random.choice(listdir)
png_uri = DataURI.from_file(image)

async def change(token):
    #avatar에 사진 여러장 넣고 랜덤으로 뽑을거면 위에 listdir~png_uri여기로 옮기셈
    
    jsondata = {
    # 'username':'Supporter', #username 
    # 'password' : token.split(':')[1] username하구 password는 토큰 형식이 이메일:비번:토큰 형식이어야함
    # 같은 원리로 result 리퀘부분에도 token.split(':')[2]로 바꾸셈
    'avatar': png_uri,
    'bio':'내소개'
    }
    # data = {'status': "online", 'custom_status': 
    # {'text': "외주 받습니다"}} #상메, 상태설정
    try:
        result = requests.patch('https://discord.com/api/v9/users/@me', json=jsondata, headers={'Authorization': token}).json()
        # requests.patch('https://discord.com/api/v9/users/@me/settings', json=data, headers={'Authorization': token}).json()
        if ('avatar' in result):
            print(f'{token} | avatar changed')
        elif ('Rate' in result):
            print('Rate limited. I will sleeping during 5 second')
            time.sleep(5)
        else:
            print(f'{token} | avatar not changed')
    except:
        print('Rate limited. I will sleeping during 5 second')
        time.sleep(5)

f = open('tokens.txt', 'r')
tokens = f.read().split('\n')
f.close()

for token in tokens:
    def temp_run():
        asyncio.run(change(token))
    
    threading.Thread(target=temp_run, args=()).start()

