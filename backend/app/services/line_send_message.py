#Module
import json
import os
import sys

import requests


# LINE 메시지 보내기 함수
def send_line_message(channel_access_token, user_to_send_id, message):
    url = 'https://api.line.me/v2/bot/message/push'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
        #'X-Line-Retry-Key':'Uaecc6981aace6cd3c6788ffb6019f1ff'
    }
    
    data = {
        'to': user_to_send_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"LINE 응답: {response.text}, 상태 코드: {response.status_code}")
    return response.status_code==200

#.env환경설정
CHANNEL_ACCESS_TOKEN="U5mOtIoUbFJ5K9L1cZJ3bqiMEEbA/aRriHqEU4IEntdiu4D7Ncr+C5YwxWSzAYAnXVYTNCDSbaC+rQdrxO/Lsjv7/bXOaqyFBqxxRVJp2IDwFMd1VgIhFfU0UMXK2YlPBISylCrSCK5K+h1xDCXdKgdB04t89/1O/w1cDnyilFU="
USER_ID="Uaecc6981aace6cd3c6788ffb6019f1ff" #Reciever


#message="안녕하세요! LINE 메시지 테스트입니다."
#send_line_message(CHANNEL_ACCESS_TOKEN, USER_ID, message)