# LLM-projects
NIPA-Google 
dev

```
LLM-projects/
  ├── backend/                            # 백엔드 (FastAPI)
  │   ├── app/
  │   │   ├── config/
  │   │   │   └── mysql_config.py         # MySQL 설정
  │   │   ├── services/
  │   │   │   ├── db_service.py           # MySQL 서비스
  │   │   │   ├── line_send_message.py    # LINE 서비스
  │   │   │   └── LLM_projects/            # LLM 서비스
  |   |   |       └──
  │   │   ├── routes/
  |   |   |   ├── __init__.py
  |   |   |   ├── attendace.py
  |   |   |   ├── students.py      
  │   │   │   ├── medication.py           # 약 API
  │   │   │   ├── schedule.py             # 일정 API
  │   │   │   └── root.py                 # 기본 루트
  │   │   ├── __init__.py
  │   │   └── main.py                     # FastAPI 앱
  │   └── venv/
  ├── src/                                # 프론트엔드 (Vue.js)
  │   ├── components/                     # Vue 컴포넌트
  │   │   ├── medication/
  │   │   │   ├── MedicationForm.vue  # 복약 입력 폼
  │   │   │   └── MedicationTable.vue # 복약 테이블 (추정)
  │   │   ├── Schedule/
  │   │   │   ├── Calendar.vue       # 캘린더 컴포넌트
  │   │   │   └── ScheduleForm.vue   # 일정 입력 폼
  │   │   └── notification/
  │   │       └── NotificationPreview.vue  # 알림 미리보기
  │   ├── layouts/
  │   │   └── DefaultLayout.vue
  │   ├── modules/
  │   │   └── axios.js     # Axios 설정
  │   ├── pages/           # 페이지 컴포넌트
  │   │   ├── Home.vue
  │   │   ├── MedicationPage.vue  # 복약 페이지
  │   │   └── SchedulePage.vue    # 일정 페이지
  │   ├── router/
  │   │   ├── index.js     # Vue Router 설정
  │   ├── store/
  │   │   └── medication.js
  │   │   └── schedule.js 
  │   ├── main.js          # Vue 앱 진입점
  │   └── vite.config.js   # Vite 설정 (포트 등)
  └── (기타 파일: package.json, README.md 등)
```
`npm install vite --save-dev`
`npm install vue-router@4 (vue3는 @4와 연동)`
`npm install cors`
`npm install axios`
