<template>
  <div class="dashboard">
    <div class="logo-container">
      <h1>🫘 Jellybean Letter</h1>
      <p class="intro">
        유치원 선생님을 위한 알림 자동화 서비스입니다.<br>
        출결 관리와 일정 알림을 간편하게 처리해 드립니다.<br>
        학부모와의 소통을 더 쉽게 만들어 줍니다.
      </p>
    </div>

    <div v-if="!isIntro" class="content">
      <div class="horizontal-layout">
        <!-- 학생 수 -->
        <div class="card">
          <h3>👦 전체 학생 수</h3>
          <p>{{ totalStudents }} 명</p>
        </div>

        <!-- 날씨 정보 -->
        <div class="card">
          <h3>🌤️ 현재 날씨</h3>
          <p>{{ weather.temperature }}°C</p>
          <p>{{ weather.description }}</p>
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

      <!-- 전체 스케줄 섹션 (실외만 표시) -->
      <div class="all-schedules">
        <h2>📅 실외 일정 (최근 4일)</h2>
        <table>
          <thead>
            <tr>
              <th>날짜</th>
              <th>시간 (분)</th>
              <th>프로그램</th>
              <th>실외 여부</th>
              <th>담당 교사</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="schedule in outdoorSchedules" :key="schedule.datetime">
              <td>{{ formatDate(schedule.datetime) }}</td>
              <td>{{ schedule.minutes }}</td>
              <td>{{ schedule.program }}</td>
              <td>{{ schedule.isoutside ? '예' : '아니오' }}</td>
              <td>{{ schedule.teacher }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 변경된 스케줄 섹션 -->
      <div class="changed-schedules" v-if="changedSchedules.length">
        <h2>🔄 변경된 야외 스케줄</h2>
        <table>
          <thead>
            <tr>
              <th>날짜</th>
              <th>시간 (분)</th>
              <th>프로그램</th>
              <th>야외 여부</th>
              <th>담당 교사</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="schedule in changedSchedules" :key="schedule.datetime">
              <td>{{ formatDate(schedule.datetime) }}</td>
              <td>{{ schedule.minutes }}</td>
              <td>{{ schedule.program }}</td>
              <td>{{ schedule.isoutside ? '예' : '아니오' }}</td>
              <td>{{ schedule.teacher }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="no-changes">🔄 변경된 스케줄이 없습니다.</p>

      <div class="button-container">
        <router-link to="/schedule" @click="logClick('Schedule')" class="action-button primary">
          📅 일정
        </router-link>
        <router-link to="/medication" @click="logClick('Medication')" class="action-button secondary">
          💊 복약
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/modules/axios.js';
import { computed, onMounted, ref } from "vue";

const totalStudents = ref(0);
const weather = ref({ temperature: 0, description: "불러오는 중..." });
const weeklySchedule = ref([]);
const changedSchedules = ref([]);
const allSchedules = ref([]);
const isIntro = ref(true);

// 오늘부터 4일간의 실외 일정 필터링
const outdoorSchedules = computed(() => {
  const today = new Date();
  const fourDaysLater = new Date(today);
  fourDaysLater.setDate(today.getDate() + 3); // 오늘 포함 4일

  return allSchedules.value
    .filter(schedule => schedule.isoutside === 1)
    .filter(schedule => {
      const scheduleDate = new Date(schedule.datetime);
      return scheduleDate >= today && scheduleDate <= fourDaysLater;
    })
    .sort((a, b) => new Date(a.datetime) - new Date(b.datetime)); // 날짜순 정렬
});

onMounted(async () => {
  try {
    const res = await api.get("http://127.0.0.1:8000/");
    totalStudents.value = res.data.total_students;
  } catch (error) {
    console.error("Root fetch failed:", error);
  }

  // 전체 스케줄 가져오기
  try {
    const response = await api.get("http://127.0.0.1:8000/schedule/api/schedules");
    console.log("받은 데이터:", response.data); // 디버깅용
    allSchedules.value = response.data;
  } catch (error) {
    console.error("전체 스케줄 불러오기 실패:", error);
  }

  // 변경된 스케줄 가져오기
  try {
    const response = await api.get("http://127.0.0.1:8000/schedule/api/changed-schedules", {
      params: { nx: 62, ny: 126 },
    });
    changedSchedules.value = response.data.changed_schedules;
  } catch (error) {
    console.error("변경된 스케줄 불러오기 실패:", error);
  }

  setTimeout(() => {
    isIntro.value = false;
  }, 3000);
});

const logClick = (page) => {
  console.log(`${page} 버튼이 클릭되었습니다.`);
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>

<style scoped>
.dashboard {
  padding: 25px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
  position: relative;
  min-height: 100vh;
}

.dashboard {
  padding: 25px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
  position: relative;
}

.logo-container {
  text-align: center;
  margin-bottom: 40px;
}

.logo-container h1 {
  font-family: 'Poppins', sans-serif;
  font-size: 4rem;
  font-weight: 700;
  background: linear-gradient(45deg, #ff6f61, #ffb88c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 2px 2px 5px rgba(255, 111, 97, 0.3);
  margin: 0;
}

.intro {
  font-size: 1.3rem;
  font-weight: 600;
  color: #4a4a4a;
  line-height: 1.6;
  margin-top: 20px;
  margin-bottom: 20px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.action-button {
  padding: 10px 20px;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none; /* 링크 기본 스타일 제거 */
  display: inline-block; /* 링크를 버튼처럼 보이게 */
}

.action-button.primary {
  background-color: #ff6f61;
  color: white;
}

.action-button.primary:hover {
  background-color: #e65a50;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.3);
}

.action-button.secondary {
  background-color: #ffffff;
  color: #ff6f61;
  border: 2px solid #ff6f61;
}

.action-button.secondary:hover {
  background-color: #fff5f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.2);
}

.content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.horizontal-layout {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  flex-wrap: nowrap;
}

.card,
.schedule {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 20px;
  border-radius: 12px;
  flex: 1;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  min-width: 0;
}

.card:hover,
.schedule:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.2);
}

h3 {
  font-size: 1.2rem;
  color: #4a4a4a;
  margin-bottom: 10px;
}

.card p {
  font-size: 1.2rem;
  color: #ff6f61;
  font-weight: 500;
}

.schedule h2 {
  font-size: 1.5rem;
  color: #4a4a4a;
  margin-bottom: 15px;
}

ul {
  list-style: none;
  padding: 0;
  max-height: 150px;
  overflow-y: auto;
}

.schedule ul li {
  font-size: 1rem;
  color: #4a4a4a;
  margin: 8px 0;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.schedule ul li:hover {
  color: #ff6f61;
  background-color: #fff5f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.2);
}

@media (max-width: 768px) {
  .dashboard {
    padding: 15px;
  }

  .logo-container h1 {
    font-size: 2.5rem;
  }

  .intro {
    font-size: 1.1rem;
  }

  .button-container {
    flex-direction: column;
    gap: 10px;
  }

  .action-button {
    width: 100%;
  }

  .horizontal-layout {
    flex-direction: column;
    gap: 15px;
  }
}

.all-schedules {
  margin-top: 30px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.all-schedules:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.2);
}

.all-schedules h2 {
  font-size: 1.5rem;
  color: #4a4a4a;
  margin-bottom: 15px;
}

.changed-schedules {
  margin-top: 30px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.changed-schedules:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.2);
}

.changed-schedules h2 {
  font-size: 1.5rem;
  color: #4a4a4a;
  margin-bottom: 15px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  font-weight: 600;
  color: #4a4a4a;
}

.no-changes {
  margin-top: 20px;
  font-size: 1.1rem;
  color: #4a4a4a;
  text-align: center;
}

@media (max-width: 768px) {
  .all-schedules, .changed-schedules {
    margin-top: 15px;
  }

  table {
    font-size: 0.9rem;
  }

  th, td {
    padding: 6px;
  }
}
</style>