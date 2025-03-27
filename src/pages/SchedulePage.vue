<template>
  <div class="schedule-page">
    <!-- 왼쪽: 일정 입력 및 스케줄 표 -->
    <div class="left-section">
      <h2>📅 일정 입력</h2>
      <ScheduleForm @updateNotification="updateNotificationText" />
      <div class="weather-debug">
        <h3>🌤️ 디버깅용 날씨 입력 (1시간 단위 시뮬레이션)</h3>
        <p>현재 시각: {{ currentTime }}</p>
        <input v-model.number="debugTemp" type="number" placeholder="온도 (°C)" />
        <input v-model.number="debugPrecip" type="number" step="0.1" placeholder="강수량 (mm)" />
        <button @click="updateSchedulesBasedOnWeather(debugTemp, debugPrecip)">오후 5시 시뮬레이션</button>
      </div>
      <div class="all-schedules">
        <h3>📅 최근 4일 일정 (실내/실외)</h3>
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

    <!-- 가운데: 수동 알림 미리보기 -->
    <div class="middle-section">
      <h2>📢 일정변경 메세지</h2>
      <div class="preview-row">
        <NotificationPreview :message="notificationText" title="📢 일정변경 메세지" />
      </div>
      <button class="action-button" @click="sendManualNotification">📩 수동 문자 보내기</button>
    </div>

    <!-- 오른쪽: 날씨 기반 알림 -->
    <div class="right-section">
      <h2>🌤️ 날씨 & 변경되는 일정</h2>
      <div class="preview-row">
        <NotificationPreview :message="weatherNotificationText" />
      </div>
      <div v-if="changedSchedules.length" class="report-section">
        <h3>🔄 변경된 일정</h3>
        <table>
          <thead>
            <tr>
              <th>날짜</th>
              <th>시간</th>
              <th>프로그램</th>
              <th>원래</th>
              <th>변경 후</th>
              <th>사유</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in changedSchedules" :key="s.datefcst">
              <td>{{ formatDateSimple(s.datefcst) }}</td>
              <td>{{ s.minutes }}</td>
              <td>{{ s.program }}</td>
              <td>{{ s.originalIsOutside ? '실외' : '실내' }}</td>
              <td>{{ s.isoutside ? '실외' : '실내' }}</td>
              <td>{{ s.weather_reason }}</td>
            </tr>
          </tbody>
        </table>
        <div class="change-notice">
          <h3>📝 수업 일정 변경 안내</h3>
          <p>{{ generateChangeNotice() }}</p>
        </div>
      </div>
      <!-- 수정: 변경된 일정이 없을 때 백엔드 메시지 표시 -->
      <p v-else class="no-changes">{{ weatherNotificationText || '🔄 변경된 일정이 없습니다' }}</p>
      <button class="action-button" @click="sendWeatherNotification">📩 날씨 문자 보내기</button>
    </div>
  </div>
</template>

<script setup>
import ScheduleForm from "@/components/Schedule/ScheduleForm.vue";
import NotificationPreview from "@/components/notification/NotificationPreview.vue";
import api from "@/modules/axios.js";
import { computed, onMounted, ref } from "vue";

const notificationText = ref("");
const weatherNotificationText = ref("");
const changedSchedules = ref([]);
const allSchedules = ref([]);
const debugTemp = ref(26);
const debugPrecip = ref(0.2);
const currentTime = ref("");

onMounted(() => {
  fetchAllSchedules();
  updateCurrentTime();
  setInterval(updateCurrentTime, 60000);
});

const recentSchedules = computed(() => {
  const today = new Date();
  const fourDaysLater = new Date(today);
  fourDaysLater.setDate(today.getDate() + 3);
  return allSchedules.value
    .filter(schedule => {
      const scheduleDate = new Date(schedule.datetime);
      return scheduleDate >= today && scheduleDate <= fourDaysLater;
    })
    .sort((a, b) => new Date(a.datetime) - new Date(b.datetime));
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
    console.log("변경된 스케줄 요청 시작:", { nx: 62, ny: 126 });
    const response = await api.get("/schedule/api/changed-schedules", {
      params: { nx: 62, ny: 126 },
      timeout: 30000,
    });
    console.log("변경된 스케줄 응답:", response.data);

    // 응답 데이터 확인 및 처리
    if (response.data && Array.isArray(response.data.items) && response.data.items.length > 0) {
      changedSchedules.value = response.data.items.map(s => ({
        datefcst: s.datefcst,
        minutes: s.minutes,
        program: s.program,
        isoutside: s.isoutside,
        originalIsOutside: s.originalIsOutside,
        teacher: s.teacher,
        weather_reason: s.weather_reason,
      }));
      weatherNotificationText.value = response.data.message || "변경된 스케줄이 있습니다.";
    } else {
      changedSchedules.value = [];
      // 백엔드에서 제공한 메시지를 weatherNotificationText에 설정
      weatherNotificationText.value = response.data.message || "안녕하세요, 학부모님!\n\n현재 날씨에 따라 변경된 스케줄이 없습니다. 아이들이 평소처럼 즐겁게 지낼 예정이에요.\n\n감사합니다!";
    }

    for (const schedule of changedSchedules.value) {
      await updateScheduleInDB(schedule);
    }
    await fetchAllSchedules();
  } catch (error) {
    console.error("변경된 스케줄 가져오기 실패:", error);
    weatherNotificationText.value = "변경된 스케줄을 가져오지 못했습니다. 백엔드 오류를 확인해주세요.";
    changedSchedules.value = [];
  }
};

const updateScheduleInDB = async (schedule) => {
  try {
    await api.put("/schedule/api/schedules", {
      datetime: schedule.datefcst,
      isoutside: schedule.isoutside,
    });
    console.log(`DB 업데이트 성공: ${schedule.datefcst} - isoutside: ${schedule.isoutside}`);
  } catch (error) {
    console.error("DB 업데이트 실패:", error);
  }
};

const generateChangeNotice = () => {
  let notice = "학부모님께,\n\n아래와 같이 수업 일정이 변경되었습니다:\n";
  changedSchedules.value.forEach(s => {
    notice += `- ${formatDateSimple(s.datefcst)} ${s.program}: ${s.originalIsOutside ? '실외' : '실내'} → ${s.isoutside ? '실외' : '실내'} (${s.weather_reason})\n`;
  });
  notice += "\n감사합니다.\nJellybean Letter";
  return notice;
};

const sendManualNotification = async () => {
  if (!notificationText.value) {
    alert("⚠️ 수동 메시지가 없습니다!");
    return;
  }
  try {
    const res = await api.post("/schedule/api/send_line", {
      message: notificationText.value,
      user_id: "Uaecc6981aace6cd3c6788ffb6019f1ff",
    });
    alert(`📩 ${res.data.message}`);
    notificationText.value = "";
  } catch (error) {
    alert("📩 전송 실패!");
  }
};

const sendWeatherNotification = async () => {
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
    alert("📩 전송 실패!");
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
  display: flex;
  width: 95%;
  margin: 20px auto;
  gap: 10px;
}

.left-section, .middle-section, .right-section {
  flex: 1;
  padding: 20px;
  border-radius: 10px;
  background: #f8f9fa;
}

.middle-section {
  background: #ffffff;
}

.right-section {
  background: #f0f8ff;
}

.weather-debug {
  margin: 20px 0;
}

.weather-debug input {
  padding: 8px;
  margin-right: 10px;
  border-radius: 5px;
  width: 100px;
}

.weather-debug button {
  padding: 8px 15px;
  background-color: #ff6f61;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.preview-row {
  display: flex;
  align-items: center;
  width: 100%;
}

.all-schedules {
  margin-top: 20px;
}

.all-schedules h3 {
  font-size: 1.4rem;
  color: #4a4a4a;
  margin-bottom: 10px;
}

.table-wrapper {
  max-height: 300px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
  table-layout: fixed;
}

th, td {
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

.report-section {
  margin-top: 20px;
  width: 100%;
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

.no-changes {
  font-size: 1rem;
  color: #4a4a4a;
  text-align: center;
  margin-top: 10px;
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
</style>