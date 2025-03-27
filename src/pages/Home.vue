<template>
  <div class="dashboard">
    <div class="logo-container" :class="{ 'fade-out': !isIntro }">
      <h1>🫘 Jellybean Letter</h1>
      <p class="intro">
        유치원 선생님을 위한 알림 자동화 서비스입니다.<br>
        출결 관리와 일정 알림을 간편하게 처리해 드립니다.<br>
        학부모와의 소통을 더 쉽게 만들어 줍니다.
      </p>
    </div>

    <div v-if="!isIntro" class="content" :class="{ 'fade-in': !isIntro }">
      <h2 class="content-logo">🫘 Jellybean Letter</h2>
      <div class="horizontal-layout">
        <div class="left-column">
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
        </div>

        <!-- 주간 일정 (실외 일정과 변경된 스케줄만 표시) -->
        <div class="schedule">
          <!-- 실외 일정 섹션 -->
          <div class="all-schedules">
            <h3>📅 실외 일정 (최근 4일)</h3>
            <div class="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>날짜</th>
                    <th>시간</th>
                    <th>프로그램</th>
                    <th>실외</th>
                    <th>교사</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="outdoorSchedules.length === 0">
                    <td colspan="5">최근 4일간 실외 일정 없음</td>
                  </tr>
                  <tr v-else v-for="schedule in outdoorSchedules" :key="schedule.datetime">
                    <td>{{ formatDateSimple(schedule.datetime) }}</td>
                    <td>{{ schedule.minutes }}</td>
                    <td>{{ schedule.program }}</td>
                    <td>{{ schedule.isoutside ? '예' : '아니오' }}</td>
                    <td>{{ schedule.teacher }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- 변경된 스케줄 섹션 -->
          <div class="changed-schedules" v-if="changedSchedules.length">
            <h3>🔄 변경된 야외 스케줄</h3>
            <div class="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>날짜</th>
                    <th>시간</th>
                    <th>프로그램</th>
                    <th>야외</th>
                    <th>교사</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="schedule in changedSchedules" :key="schedule.datetime">
                    <td>{{ formatDateSimple(schedule.datetime) }}</td>
                    <td>{{ schedule.minutes }}</td>
                    <td>{{ schedule.program }}</td>
                    <td>{{ schedule.isoutside ? '예' : '아니오' }}</td>
                    <td>{{ schedule.teacher }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <p v-else class="no-changes">🔄 변경된 스케줄이 없습니다.</p>
        </div>
      </div>

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

const outdoorSchedules = computed(() => {
  const today = new Date();
  const fourDaysLater = new Date(today);
  fourDaysLater.setDate(today.getDate() + 3);

  return allSchedules.value
    .filter(schedule => schedule.isoutside === 1)
    .filter(schedule => {
      const scheduleDate = new Date(schedule.datetime);
      return scheduleDate >= today && scheduleDate <= fourDaysLater;
    })
    .sort((a, b) => new Date(a.datetime) - new Date(b.datetime));
});

// 날씨 상태 변환 함수
const getWeatherDescription = (skyCode) => {
  switch (skyCode) {
    case '1': return '맑음';
    case '3': return '구름많음';
    case '4': return '흐림';
    default: return '알 수 없음';
  }
};

onMounted(async () => {
  try {
    const res = await api.get("http://127.0.0.1:8000/");
    totalStudents.value = res.data.total_students;
  } catch (error) {
    console.error("Root fetch failed:", error);
  }

  // 날씨 데이터 가져오기
  try {
    const weatherResponse = await api.get("http://127.0.0.1:8000/weather", {
      params: { nx: 62, ny: 126 } // 서울 좌표 예시
    });
    weather.value.temperature = weatherResponse.data.temperature;
    weather.value.description = getWeatherDescription(weatherResponse.data.sky);
  } catch (error) {
    console.error("날씨 데이터 불러오기 실패:", error);
    weather.value.description = "날씨 정보 없음";
  }

  try {
    const response = await api.get("http://127.0.0.1:8000/schedule/api/schedules");
    allSchedules.value = response.data;
  } catch (error) {
    console.error("전체 스케줄 불러오기 실패:", error);
  }

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

const formatDateSimple = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString("ko-KR", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 처음 로고와 안내문 중앙 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  min-height: 100vh; /* 전체 화면 높이 */
  padding: 25px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
}

.logo-container {
  text-align: center;
  transition: opacity 0.5s ease;
}

.logo-container.fade-out {
  opacity: 0;
}

.logo-container h1 {
  font-family: 'Poppins', sans-serif;
  font-size: 6rem;
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
}

.content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  opacity: 0;
  transition: opacity 0.5s ease;
  width: 100%;
  position: relative;
  top: -94px; /* 전체 콘텐츠를 2.5cm(약 94px) 위로 이동 */
}

.content.fade-in {
  opacity: 1;
}

.content-logo {
  font-family: 'Poppins', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #ff6f61, #ffb88c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-align: center;
  position: absolute; /* 최상단 고정 */
  top: -60px; /* 콘텐츠 상단에서 약간 위로 */
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
}

.horizontal-layout {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  width: 100%;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
}

.card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.card:hover {
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

.schedule {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 20px;
  border-radius: 12px;
  flex: 3;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.schedule:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.2);
}

.all-schedules,
.changed-schedules {
  margin-top: 10px;
}

.all-schedules h3,
.changed-schedules h3 {
  font-size: 1.4rem;
  color: #4a4a4a;
  margin-bottom: 10px;
}

.table-wrapper {
  max-height: 200px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
}

th, td {
  border: 1px solid #e0e0e0;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #ff6f61;
  color: white;
  font-weight: 600;
}

td {
  color: #4a4a4a;
}

tbody tr:hover {
  background-color: #fff5f5;
  transition: background-color 0.2s ease;
}

.no-changes {
  font-size: 1rem;
  color: #4a4a4a;
  text-align: center;
  margin-top: 10px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.action-button {
  padding: 10px 20px;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
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

@media (max-width: 768px) {
  .dashboard {
    padding: 15px;
  }

  .logo-container h1 {
    font-size: 4rem;
  }

  .content-logo {
    font-size: 2rem;
    top: -50px; /* 모바일에서 조금 더 위로 */
  }

  .content {
    top: -70px; /* 모바일에서 약간 덜 올리기 */
  }

  .intro {
    font-size: 1.1rem;
  }

  .horizontal-layout {
    flex-direction: column;
    gap: 15px;
  }

  .schedule {
    flex: 1;
  }

  .button-container {
    flex-direction: column;
    gap: 10px;
  }

  .action-button {
    width: 100%;
  }

  table {
    font-size: 0.9rem;
  }

  th, td {
    padding: 8px;
  }
}
</style>