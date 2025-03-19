<template>
  <div class="dashboard">
    <h1>🏫 유치원 대시보드</h1>

    <div class="cards">
      <!-- 학생 수 -->
      <div class="card">
        <h3>👦 전체 학생 수</h3>
        <p>{{ totalStudents }} 명</p>
      </div>

      <!-- 출결 현황 -->
      <div class="card">
        <h3>📅 오늘 출결 현황</h3>
        <ul>
          <li>✅ 출석: {{ attendance.present }} 명</li>
          <li>⏰ 지각: {{ attendance.late }} 명</li>
          <li>🚫 결석: {{ attendance.absent }} 명</li>
        </ul>
      </div>

      <!-- 날씨 정보 -->
      <div class="card">
        <h3>🌤️ 현재 날씨</h3>
        <p>{{ weather.temperature }}°C</p>
        <p>{{ weather.description }}</p>
      </div>
    </div>

    <!-- 주간 일정 -->
    <div class="schedule">
      <h2>🗓 이번 주 일정</h2>
      <ul>
        <li v-for="event in weeklySchedule" :key="event.id">
          {{ event.date }} - {{ event.name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// ✅ 1️⃣ ref 변수를 먼저 선언
const totalStudents = ref(0);
const attendance = ref({ present: 0, late: 0, absent: 0 });
const weather = ref({ temperature: 0, description: "불러오는 중..." });
const weeklySchedule = ref([]);

// ✅ 2️⃣ Mock 데이터 적용 (초기값 설정)
function setMockData() {
  totalStudents.value = 30; // 학생 30명
  attendance.value = { present: 25, late: 3, absent: 2 };
  weather.value = { temperature: 22, description: "맑음" };
  weeklySchedule.value = [
    { id: 1, date: "2025-03-20", name: "소풍" },
    { id: 2, date: "2025-03-22", name: "체육대회" }
  ];
}

// ✅ 3️⃣ API 요청 함수
async function fetchDashboardData() {
  try {
    // 🎯 API 요청 전에 Mock 데이터 적용 (UI 깜빡임 방지)
    setMockData();

    // 🔹 학생 수 데이터 가져오기
    const studentRes = await axios.get("/api/students/count");
    totalStudents.value = studentRes.data.count || 30;

    // 🔹 오늘 출결 현황 가져오기
    const attendanceRes = await axios.get("/api/attendance/today");
    attendance.value = attendanceRes.data || { present: 25, late: 3, absent: 2 };

    // 🔹 날씨 정보 가져오기 (임시 API 사용)
    const weatherRes = await axios.get("https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current_weather=true");
    weather.value.temperature = weatherRes.data.current_weather.temperature || 22;
    weather.value.description = weatherRes.data.current_weather.weathercode || "맑음";

    // 🔹 주간 일정 가져오기
    const scheduleRes = await axios.get("/api/schedule/week");
    weeklySchedule.value = scheduleRes.data || [
      { id: 1, date: "2025-03-20", name: "소풍" },
      { id: 2, date: "2025-03-22", name: "체육대회" }
    ];
  } catch (error) {
    console.error("대시보드 데이터 불러오기 실패:", error);
  }
}

// ✅ 4️⃣ 컴포넌트가 마운트되면 데이터 로딩
onMounted(fetchDashboardData);
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.cards {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  flex: 1;
  text-align: center;
  min-width: 200px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 10px;
}

.schedule {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

ul {
  list-style: none;
  padding: 0;
}

@media (max-width: 768px) {
  .cards {
    flex-direction: column;
  }
}
</style>
