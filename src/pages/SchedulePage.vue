<template>
  <div class="schedule-page">
    <!-- 상단 로고 -->
    <div class="header">
      <h1 class="logo">🫘 Jellybean Letter</h1>
      <hr class="divider" />
    </div>

    <!-- 콘텐츠 영역 -->
    <div class="content-container">
      <!-- 왼쪽: 최근 4일 일정 -->
      <div class="left-section">
        <div class="section">
          <h2>📅 최근 4일 일정 (실내/실외)</h2>
          <div v-if="isLoading">로딩 중...</div>
          <div v-else class="table-wrapper">
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
                <tr v-if="recentSchedules.length === 0">
                  <td colspan="5">최근 4일간 일정 없음</td>
                </tr>
                <tr v-else v-for="schedule in recentSchedules" :key="schedule.datetime">
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
      </div>

      <!-- 세로 구분선 -->
      <div class="vertical-divider"></div>

      <!-- 오른쪽: 탭 영역 -->
      <div class="right-section">
        <div class="tab-container">
          <div class="tab-buttons">
            <button
              :class="{ active: activeTab === 'schedule' }"
              @click="activeTab = 'schedule'"
            >
              일정 변경 안내문 생성기
            </button>
            <button
              :class="{ active: activeTab === 'weather' }"
              @click="activeTab = 'weather'"
            >
              날씨 기반 자동 안내문 생성기
            </button>
          </div>

          <!-- 탭 1: 일정 변경 안내문 생성기 -->
          <div v-if="activeTab === 'schedule'" class="tab-content">
            <div class="section schedule-input-section">
              <ScheduleForm @updateNotification="updateNotificationText" />
            </div>
            <div class="section">
              <h2>📢 일정변경 메세지</h2>
              <NotificationPreview :message="notificationText" />
              <label>
                <input type="checkbox" v-model="keepNotificationText"> 전송 후 메시지 유지
              </label>
              <button
                class="action-button"
                type="button"
                @click="sendManualNotification"
                :disabled="isSending"
              >
                {{ isSending ? '전송 중...' : '📩 수동 문자 보내기' }}
              </button>
            </div>
          </div>

          <!-- 탭 2: 날씨 기반 자동 안내문 생성기 -->
          <div v-if="activeTab === 'weather'" class="tab-content">
          <div class="section">
            <h2>🌤️ 디버깅용 날씨 입력</h2>
            <p>현재 시각: {{ currentTime }}</p>
            <input v-model.number="debugTemp" type="number" placeholder="온도 (°C)" />
            <input v-model.number="debugPrecip" type="number" step="0.1" placeholder="강수량 (mm)" />
            <button @click="updateSchedulesBasedOnWeather(debugTemp, debugPrecip)">
              오후 5시 시뮬레이션
            </button>
          </div>
          <div class="section">
            <h2>🌤️ 날씨 & 변경되는 일정</h2>
            <NotificationPreview :message="weatherNotificationText" />
            <div class="weather-table-section">
              <h3>🌡️ 현재 날씨 정보</h3>
              <table>
                <thead>
                  <tr>
                    <th>온도 (°C)</th>
                    <th>강수량 (mm)</th>
                    <th>업데이트 시각</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ debugTemp }}</td>
                    <td>{{ debugPrecip }}</td>
                    <td>{{ currentTime }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <button class="action-button" type="button" @click="sendWeatherNotification">
              📩 날씨 문자 보내기
            </button>
          </div>
        </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ScheduleForm from "@/components/Schedule/ScheduleForm.vue";
import NotificationPreview from "@/components/notification/NotificationPreview.vue";
import api from "@/modules/axios.js";
import { computed, onMounted, ref } from "vue";

const activeTab = ref("schedule");
const notificationText = ref("");
const weatherNotificationText = ref("");
const changedSchedules = ref([]);
const allSchedules = ref([]);
const debugTemp = ref(26);
const debugPrecip = ref(0.2);
const currentTime = ref("");
const isLoading = ref(true);
const isSending = ref(false); // 로딩 상태 추가
const keepNotificationText = ref(false); // 전송 후 메시지 유지 여부

onMounted(async () => {
  await fetchAllSchedules();
  updateCurrentTime();
  setInterval(updateCurrentTime, 60000);
  isLoading.value = false;
});

const recentSchedules = computed(() => {
  if (!allSchedules.value.length) {
    console.log("allSchedules가 비어있습니다.");
    return [];
  }

  const today = new Date();
  const fourDaysLater = new Date(today);
  fourDaysLater.setDate(today.getDate() + 3);

  const filteredSchedules = allSchedules.value
    .filter((schedule) => {
      const scheduleDate = new Date(schedule.datetime);
      const isWithinRange = scheduleDate >= today && scheduleDate <= fourDaysLater;
      console.log(`일정 필터링: ${schedule.datetime}, 범위 내: ${isWithinRange}`);
      return isWithinRange;
    })
    .sort((a, b) => new Date(a.datetime) - new Date(b.datetime));

  console.log("최근 4일 일정:", filteredSchedules);
  return filteredSchedules;
});

const fetchAllSchedules = async () => {
  try {
    const response = await api.get("/schedule/api/schedules");
    allSchedules.value = response.data;
    console.log("전체 스케줄 로드 성공:", response.data);
  } catch (error) {
    console.error("전체 스케줄 불러오기 실패:", error);
    allSchedules.value = [];
  }
};

const updateCurrentTime = () => {
  currentTime.value = new Date().toLocaleString("ko-KR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

const updateNotificationText = (message) => {
  notificationText.value = message;
};

const updateSchedulesBasedOnWeather = async (temperature, precipitation) => {
  try {
    isLoading.value = true;
    const response = await api.get("/schedule/api/changed-schedules", {
      params: { nx: 62, ny: 126 },
      timeout: 30000,
    });
    console.log("백엔드 응답:", response.data);

    if (response.data && Array.isArray(response.data.items) && response.data.items.length > 0) {
      changedSchedules.value = response.data.items.map((s) => {
        console.log("매핑된 데이터:", s);
        return {
          datefcst: s.datefcst,
          minutes: s.minutes,
          program: s.program,
          isoutside: s.isoutside,
          originalIsOutside: s.originalIsOutside,
          teacher: s.teacher,
          weather_reason: s.weather_reason,
        };
      });
      weatherNotificationText.value = response.data.message || "변경된 스케줄이 있습니다.";
      console.log("최종 changedSchedules:", changedSchedules.value);
    } else {
      changedSchedules.value = [];
      weatherNotificationText.value =
        response.data.message ||
        "안녕하세요, 학부모님!\n\n현재 날씨에 따라 변경된 스케줄이 없습니다.";
      console.log("변경된 스케줄 없음");
    }

    debugTemp.value = temperature;
    debugPrecip.value = precipitation;
    console.log("weatherNotificationText:", weatherNotificationText.value);

    for (const schedule of changedSchedules.value) {
      await updateScheduleInDB(schedule);
    }
    await fetchAllSchedules();
  } catch (error) {
    console.error("에러:", error);
    weatherNotificationText.value = "변경된 스케줄을 가져오지 못했습니다.";
    changedSchedules.value = [];
  } finally {
    isLoading.value = false;
  }
};

const updateScheduleInDB = async (schedule) => {
  try {
    await api.put("/schedule/api/schedules", {
      datetime: schedule.datefcst,
      program: schedule.program, // 고유 식별용 추가
      isoutside: schedule.isoutside,
    });
    console.log(`DB 업데이트 성공: ${schedule.datefcst} - ${schedule.program}`);
  } catch (error) {
    console.error("DB 업데이트 실패:", error);
  }
};

const generateChangeNotice = () => {
  let notice = "학부모님께,\n\n아래와 같이 수업 일정이 변경되었습니다:\n";
  changedSchedules.value.forEach((s) => {
    notice += `- ${formatDateSimple(s.datefcst)} ${s.program}: ${
      s.originalIsOutside ? "실외" : "실내"
    } → ${s.isoutside ? "실외" : "실내"} (${s.weather_reason})\n`;
  });
  notice += "\n감사합니다.\nJellybean Letter";
  return notice;
};

const sendManualNotification = async (event) => {
  event.preventDefault(); // 새로고침 방지
  if (!notificationText.value) {
    alert("⚠️ 수동 메시지가 없습니다!");
    return;
  }
  isSending.value = true;
  try {
    const res = await api.post("/schedule/api/send_line", {
      message: notificationText.value,
      user_id: "Uaecc6981aace6cd3c6788ffb6019f1ff",
    });
    alert(`📩 ${res.data.message}`);
    if (!keepNotificationText.value) {
      notificationText.value = ""; // 체크박스가 꺼져 있을 때만 초기화
    }
  } catch (error) {
    alert("📩 전송 실패!");
    console.error("수동 문자 전송 실패:", error);
  } finally {
    isSending.value = false;
  }
};

const sendWeatherNotification = async (event) => {
  event.preventDefault(); // 새로고침 방지 (날씨 문자 보내기에도 적용)
  if (!weatherNotificationText.value) {
    alert("⚠️ 날씨 메시지가 없습니다!");
    return;
  }
  try {
    const res = await api.post("/schedule/api/send_line", {
      message: weatherNotificationText.value,
      user_id: "Uaecc6981aace6cd3c6788ffb6019f1ff",
    });
    alert(`📩 ${res.data.message}`);
  } catch (error) {
    alert("📩 전송 personally!");
    console.error("날씨 문자 전송 실패:", error);
  }
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
.schedule-page {
  width: 95%;
  margin: 20px auto;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  font-family: "Poppins", sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #ff6f61, #ffb88c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 2px 2px 5px rgba(255, 111, 97, 0.3);
  margin: 0;
}

.divider {
  border: 1px solid #ddd;
  margin: 10px 0;
}

.content-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.left-section,
.right-section {
  flex: 1;
  min-width: 0;
}

.vertical-divider {
  width: 2px;
  background-color: #ddd;
  margin: 0 10px;
}

.tab-container {
  width: 100%;
}

.tab-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-buttons button {
  padding: 10px 20px;
  font-size: 1.1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #e9ecef;
  color: #4a4a4a;
  transition: background-color 0.3s;
}

.tab-buttons button.active {
  background-color: #ff6f61;
  color: white;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.section {
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.section h2 {
  font-size: 1.5rem;
  color: #4a4a4a;
  margin-bottom: 15px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
  table-layout: fixed;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  word-wrap: break-word;
}

th {
  background-color: #ff6f61;
  color: white;
  font-weight: 600;
}

td {
  color: #4a4a4a;
}

.section input {
  padding: 8px;
  margin-right: 10px;
  border-radius: 5px;
  width: 100px;
}

.section button {
  padding: 8px 15px;
  background-color: #ff6f61;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.report-section {
  margin-top: 20px;
}

.change-notice {
  margin-top: 15px;
}

.change-notice p {
  white-space: pre-wrap;
  background: #fff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.action-button {
  margin-top: 15px;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  width: 100%;
  text-align: center;
}

.action-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }

  .vertical-divider {
    display: none;
  }

  .logo {
    font-size: 2rem;
  }
}
</style>