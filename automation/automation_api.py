#Module 분석환경 통합
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import re
import openai

#dummy data
dummy_schedule_data = """
datetime,minutes,program,isoutside,teacher
2025-03-27 08:30:00,30,Play - Free Choice,False,Ms. Sophia
2025-03-27 09:00:00,30,Morning Circle Time,False,Ms. Emma
2025-03-27 09:30:00,30,Physical Development (Gym),True,Mr. Daniel
2025-03-27 10:00:00,30,Morning Snack,False,Ms. Emily
2025-03-27 10:30:00,30,Teacher Initiated Activity (English Language),False,Mr. Daniel
2025-03-27 11:00:00,30,PE,True,Mr. James
2025-03-27 11:30:00,30,Lunch Time,False,Ms. Emily
2025-03-27 12:00:00,60,Brushing Teeth / Quiet Time / Nap Time,False,Ms. Sophia
2025-03-27 13:00:00,30,Music,False,Ms. Olivia
2025-03-27 13:30:00,30,Literacy,False,Mr. Daniel
2025-03-27 14:00:00,15,Afternoon Snack,False,Ms. Emily
2025-03-27 14:15:00,30,Understanding the World,False,Mr. James
2025-03-27 14:45:00,30,Child-Initiated Play,False,Mr. James
2025-03-27 15:15:00,15,End of Day Circle Time,False,Ms. Emma
2025-03-27 15:30:00,60,After School Club,True,Ms. Olivia
2025-03-28 08:30:00,30,Play - Free Choice,False,Ms. Sophia
2025-03-28 09:00:00,30,Morning Circle Time,False,Ms. Emma
2025-03-28 09:30:00,30,Expressive Art & Design,False,Ms. Olivia
2025-03-28 10:00:00,30,Morning Snack,False,Ms. Emily
2025-03-28 10:30:00,60,Park,True,Ms. Emma
2025-03-28 11:30:00,30,Lunch Time,False,Ms. Emily
2025-03-28 12:00:00,60,Brushing Teeth / Quiet Time / Nap Time,False,Ms. Sophia
2025-03-28 13:00:00,30,Child-Initiated Play,False,Mr. James
2025-03-28 13:30:00,30,Library,False,Ms. Sophia
2025-03-28 14:00:00,15,Afternoon Snack,False,Ms. Emily
2025-03-28 14:15:00,30,Show and Tell,False,Ms. Emma
2025-03-28 14:45:00,30,Mandarin,False,Ms. Sophia
2025-03-28 15:15:00,15,End of Day Circle Time,False,Ms. Emma
2025-03-28 15:30:00,60,After School Club,True,Ms. Olivia
2025-03-31 08:30:00,30,Play - Free Choice,False,Ms. Sophia
2025-03-31 09:00:00,30,Morning Circle Time,False,Ms. Emma
2025-03-31 09:30:00,30,Sing along/ Storytime,False,Ms. Olivia
2025-03-31 10:00:00,30,Morning Snack,False,Ms. Emily
2025-03-31 10:30:00,30,Teacher Initiated Activity (English Language),False,Mr. Daniel
2025-03-31 11:00:00,30,PE,True,Mr. James
2025-03-31 11:30:00,30,Lunch Time,False,Ms. Emily
2025-03-31 12:00:00,60,Brushing Teeth / Quiet Time / Nap Time,False,Ms. Sophia
2025-03-31 13:00:00,30,Child-Initiated Play,False,Mr. James
2025-03-31 13:30:00,30,Literacy,False,Mr. Daniel
2025-03-31 14:00:00,15,Afternoon Snack,False,Ms. Emily
2025-03-31 14:15:00,30,Maths,False,Mr. James
2025-03-31 14:45:00,30,Mandarin,False,Ms. Sophia
2025-03-31 15:15:00,15,End of Day Circle Time,False,Ms. Emma
2025-03-31 15:30:00,60,After School Club,True,Ms. Olivia
2025-04-01 08:30:00,30,Play - Free Choice,False,Ms. Sophia
2025-04-01 09:00:00,30,Morning Circle Time,False,Ms. Emma
2025-04-01 09:30:00,30,Physical Development (Gym),True,Mr. Daniel
2025-04-01 10:00:00,30,Morning Snack,False,Ms. Emily
2025-04-01 10:30:00,30,Teacher Initiated Activity (English Language),False,Mr. Daniel
2025-04-01 11:00:00,30,PE,True,Mr. James
2025-04-01 11:30:00,30,Lunch Time,False,Ms. Emily
2025-04-01 12:00:00,60,Brushing Teeth / Quiet Time / Nap Time,False,Ms. Sophia
2025-04-01 13:00:00,30,Music,False,Ms. Olivia
2025-04-01 13:30:00,30,Literacy,False,Mr. Daniel
2025-04-01 14:00:00,15,Afternoon Snack,False,Ms. Emily
2025-04-01 14:15:00,30,Understanding the World,False,Mr. James
2025-04-01 14:45:00,30,Child-Initiated Play,False,Mr. James
2025-04-01 15:15:00,15,End of Day Circle Time,False,Ms. Emma
2025-04-01 15:30:00,60,After School Club,True,Ms. Olivia
2025-04-02 08:30:00,30,Play - Free Choice,False,Ms. Sophia
2025-04-02 09:00:00,30,Morning Circle Time,False,Ms. Emma
2025-04-02 09:30:00,30,Expressive Art & Design,False,Ms. Olivia
2025-04-02 10:00:00,30,Morning Snack,False,Ms. Emily
2025-04-02 10:30:00,30,Teacher Initiated Activity (English Language),False,Mr. Daniel
2025-04-02 11:00:00,30,PE,True,Mr. James
2025-04-02 11:30:00,30,Lunch Time,False,Ms. Emily
2025-04-02 12:00:00,60,Brushing Teeth / Quiet Time / Nap Time,False,Ms. Sophia
2025-04-02 13:00:00,30,Child-Initiated Play,False,Mr. James
2025-04-02 13:30:00,30,Literacy,False,Mr. Daniel
2025-04-02 14:00:00,15,Afternoon Snack,False,Ms. Emily
2025-04-02 14:15:00,30,Maths,False,Mr. James
2025-04-02 14:45:00,30,Mandarin,False,Ms. Sophia
2025-04-02 15:15:00,15,End of Day Circle Time,False,Ms. Emma
2025-04-02 15:30:00,60,After School Club,True,Ms. Olivia
2025-04-03 08:30:00,30,Play - Free Choice,False,Ms. Sophia
2025-04-03 09:00:00,30,Morning Circle Time,False,Ms. Emma
2025-04-03 09:30:00,30,Physical Development (Gym),True,Mr. Daniel
2025-04-03 10:00:00,30,Morning Snack,False,Ms. Emily
2025-04-03 10:30:00,30,Teacher Initiated Activity (English Language),False,Mr. Daniel
2025-04-03 11:00:00,30,PE,True,Mr. James
2025-04-03 11:30:00,30,Lunch Time,False,Ms. Emily
2025-04-03 12:00:00,60,Brushing Teeth / Quiet Time / Nap Time,False,Ms. Sophia
2025-04-03 13:00:00,30,Music,False,Ms. Olivia
2025-04-03 13:30:00,30,Literacy,False,Mr. Daniel
2025-04-03 14:00:00,15,Afternoon Snack,False,Ms. Emily
2025-04-03 14:15:00,30,Understanding the World,False,Mr. James
2025-04-03 14:45:00,30,Child-Initiated Play,False,Mr. James
2025-04-03 15:15:00,15,End of Day Circle Time,False,Ms. Emma
2025-04-03 15:30:00,60,After School Club,True,Ms. Olivia
2025-04-04 08:30:00,30,Play - Free Choice,False,Ms. Sophia
2025-04-04 09:00:00,30,Morning Circle Time,False,Ms. Emma
2025-04-04 09:30:00,30,Expressive Art & Design,False,Ms. Olivia
2025-04-04 10:00:00,30,Morning Snack,False,Ms. Emily
2025-04-04 10:30:00,60,Park,True,Ms. Emma
2025-04-04 11:30:00,30,Lunch Time,False,Ms. Emily
2025-04-04 12:00:00,60,Brushing Teeth / Quiet Time / Nap Time,False,Ms. Sophia
2025-04-04 13:00:00,30,Child-Initiated Play,False,Mr. James
2025-04-04 13:30:00,30,Library,False,Ms. Sophia
2025-04-04 14:00:00,15,Afternoon Snack,False,Ms. Emily
2025-04-04 14:15:00,30,Show and Tell,False,Ms. Emma
2025-04-04 14:45:00,30,Mandarin,False,Ms. Sophia
2025-04-04 15:15:00,15,End of Day Circle Time,False,Ms. Emma
2025-04-04 15:30:00,60,After School Club,True,Ms. Olivia
"""


def extract_float(s):
    # 숫자, 소수점, 그리고 '-' 기호만 남기기
    numbers = re.findall(r'[-]?\d+\.\d+|[-]?\d+', s)
    if numbers:
        return float(numbers[0])
    return 0      
class WeatherActivityAdvisor:
    def __init__(self, service_key):
        """
        기상청과 대기질 API를 활용한 야외활동 적합성 판단 클래스
        
        :param service_key: 공공데이터포털에서 발급받은 서비스키
        """
        self.service_key = service_key
        self.weather_data = None
        self.df_schedule=None
        self.df_rule=None
        self.base_url_weather = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
        self.base_url_air = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc"
        now = datetime.now()
        self.base_date=now.strftime("%Y%m%d")

    def get_weather_forecast_by_date(self, nx, ny):
        """
        기상정
        """
        now = datetime.now()
        

        # region ifelif basetime
        # API는 매 3시간마다 업데이트되므로 현재 시간에 맞는 base_time 설정
        if now.hour < 2:
            base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
            base_time = "2300"
        elif now.hour < 5:
            base_time = "0200"
        elif now.hour < 8:
            base_time = "0500"
        elif now.hour < 11:
            base_time = "0800"
        elif now.hour < 14:
            base_time = "1100"
        elif now.hour < 17:
            base_time = "1400"
        elif now.hour < 20:
            base_time = "1700"
        elif now.hour < 23:
            base_time = "2000"
        else:
            base_time = "2300"
        #endregion
        
        # 여러 페이지의 데이터를 모두 수집
        all_items = []
        
        url = f"{self.base_url_weather}/getVilageFcst"
        params = {
            'serviceKey': self.service_key,
            'pageNo': str(1),
            'numOfRows': '1000',
            'dataType': 'JSON',
            'base_date': self.base_date,
            'base_time': base_time,
            'nx': nx,
            'ny': ny
        }
        
        try:
            page='1'
            response = requests.get(url, params=params)
            print(f"날씨 API 페이지 {page} 응답 상태 코드: {response.status_code}")
            
            # 응답의 내용 일부 출력하여 디버깅
            #print(f"페이지 {page_no} 응답 내용 일부: {response.text[:200]}...")
            
            if response.status_code == 200:                
                # JSON 응답 처리
                try:
                    data = response.json()
                    items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                    if items:
                        all_items.extend(items)
                    else:
                        print(f"페이지 {page} 날씨 API 응답에 데이터가 없습니다.")
                except json.JSONDecodeError as e:
                    print(f"페이지 {page} JSON 파싱 오류: {str(e)}")
                    if "SERVICE_KEY" in response.text:
                        print("서비스키 관련 오류일 수 있습니다. 서비스키를 확인해주세요.")
           
        except Exception as e:
            print(f"페이지 {page} 날씨 API 호출 중 예외 발생: {str(e)}")
        self.weather_data = pd.DataFrame(all_items)

        
        return None

    def process_weather_data(self):
        # 날씨 데이터 전처리
        # Rule based로 판단 요소: TMP(기온), WSD(풍속), POP(강수확률), PCP(강수량), SNO(적설량)
        # 메시지 내용에 포함될 내용: REH, SKY
        # Drop 시킬 정보: WAV(파고 ), UUU 풍속(동서), VEC 풍향, VVV풍속(남북)O
        df=self.weather_data

        # 필요한 column들을 정리
        df = df.pivot(index=['baseDate', "fcstDate",'fcstTime', 'nx', 'ny','baseTime'], columns='category', values='fcstValue').reset_index()
        df.insert(0,'datefcst',pd.to_datetime(df['fcstDate'].astype(str) + df['fcstTime'].str.zfill(4), format='%Y%m%d%H%M'))
        df.insert(0,'datenow',pd.to_datetime(df['baseDate'].astype(str) + df['baseTime'].str.zfill(4), format='%Y%m%d%H%M'))
        
        df['PCP'] = df['PCP'].replace('강수없음', 0)
        df['SNO'] = df['SNO'].replace('적설없음', 0)
        df['PCP']=df['PCP'].astype(str).apply(extract_float)
        df.drop(columns=['baseDate','baseTime','fcstDate','fcstTime','WAV', 'UUU','TMN','TMX', 'VEC', 'VVV'], inplace=True)
        #filtered_df = df[df['baseDate'] < df_pivot['baseDate'][0]+4
        # columns=['datenow'(datetime),'datefcst'(datetime),'nx','ny','PCP','POP','PTY','REH','SKY','SNO','T3H','WSD']
        # datetime 제외 모두 float
        # Example
        # 2025-03-26 05:00:00,2025-03-26 06:00:00,62,126,0.0,20,0,75,3,0,7,1.2
        # 2025-03-26 05:00:00,2025-03-26 07:00:00,62,126,0.0,0,0,75,1,0,6,1.1
        # to_csv대신 DB에 INSERT (중복되는 데이터와 새로생긴 데이터의 차이는 어떻게??)
        self.weather_data = df
        df.to_csv('weather_data_refined.csv', index=False)

    def decision_making(self):
        # df_rule np.where로 기상-야외활동가능여부 판단
        df_weather=pd.read_csv("weather_data_refined.csv")
        df_rule=pd.DataFrame(index=range(len(df_weather)-1))
        df_rule=df_rule.reindex(df_weather.index)
        df_rule['TMPrule1']=3
        df_rule['TMPrule2']=30
        df_rule['WSDrule']=10
        df_rule['PCPrule']=3
        df_rule['SNOrule']=2
        #TMP, WSD, POP, PCP, SNO
        df_weather['isoutside']=np.where(
            (df_weather['TMP']<df_rule['TMPrule1'])|(df_weather['TMP']>df_rule['TMPrule2'])|(df_weather['WSD'] >df_rule['WSDrule'])|(df_weather['PCP']>df_rule['PCPrule'])|(df_weather['SNO']>df_rule['SNOrule']), True, False)                                       

        # df_weather_outside로 비교
        df_weather_outside=df_weather[['datefcst','isoutside']]
        df_weather_outside['datefcst']=pd.to_datetime(df_weather_outside['datefcst'])
        
        # df_schedule_outside 추출
        # Query SELECT SCHEDULE 
        df_schedule=pd.read_csv("kindergarten_schedule.csv")
        df_schedule.rename(columns={'datetime':'datefcst'},inplace=True)
        df_schedule_outside=df_schedule[df_schedule['isoutside']==True]
        df_schedule_outside['datefcst']=pd.to_datetime(df_schedule_outside['datefcst'])
        df_schedule_outside['datefcst']=df_schedule_outside['datefcst'].dt.round('H')

        # df_weather_outside와 df_schedule_outside 비교 - inner join merge 통해
        changed_schedules=pd.merge(df_weather_outside,df_schedule_outside,on=['datefcst','isoutside'],how='inner')
        print(changed_schedules)
        # 날씨, 수업 데이터 저장 해놓기
        if(changed_schedules.empty):
            return []
        return changed_schedules
        





# main 활용 부분
if __name__=="__main__":
    advisor=WeatherActivityAdvisor(WEATHER_API_SERVICE_KEY)
    nx=62
    ny=126
    station_name="서울"
    # 꼭 순서대로 함수 사용하셔야합니다!
    # 날씨정보가져오기
    
    # DB INSERT
    advisor.get_weather_forecast_by_date(nx, ny)
    # DB SELECT decision 가능하게 날씨정보 후처리
    advisor.process_weather_data()
    prompt_data=advisor.decision_making()
    if(prompt_data==None):
        print("변경할 일정이 없습니다.")
    else:
        client=openai.Client(api_key=OPENAI_APIKEY)
        prompt=f"""
        {prompt_data} 파일에는 Program이름과 Teacher의 성함이 있어 참고해서 생성해줘


        """

        response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 친절한 유치원 선생님이고 학부모에게 변경 사항을 작성하는 역할이야."},
            {"role": "user", "content": 
                prompt
            }
        ]
        )
        print(prompt_data)





