# LLM-projects
NIPA-Google 
dev

```
LLM-projects/
  ├── backend/
  │   ├── app/
  │   │   ├── config/
  │   │   │   └── mysql_config.py    # MySQL 설정
  │   │   ├── services/
  │   │   │   ├── db_service.py     # MySQL 서비스
  │   │   │   ├── line_send_message.py    # LINE 서비스
  │   │   │   └── llm_service.py     # LLM 서비스
  │   │   ├── routes/
  │   │   │   ├── medication.py      # 약 API
  │   │   │   ├── schedule.py        # 일정 API
  │   │   │   └── root.py           # 기본 루트
  │   │   └── main.py                # FastAPI 앱
  │   └── venv/
  ├── src/
  │   └── frontend/
  │       ├── src/
  │       │   ├── modules/
  │       │   │   └── axios.js       # API 클라이언트
  │       │   ├── pages/
  │       │   │   ├── Home.vue       # 대시보드
  │       │   │   ├── Medication.vue # 약 UI
  │       │   │   └── Schedule.vue   # 일정 UI
  │       │   └── router/
  │       │       └── index.js       # 라우팅
  │       └── vite.config.js
```
