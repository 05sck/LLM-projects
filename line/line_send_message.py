#Module
import requests
import json


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
    print(response.text)
    
    return response

#.env환경설정
CHANNEL_ACCESS_TOKEN = ""
USER_ID="" #Reciever


message="안녕하세요! LINE 메시지 테스트입니다."
send_line_message(CHANNEL_ACCESS_TOKEN, USER_ID, message)
