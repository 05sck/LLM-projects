<template>
  <div class="schedule-page">
    <!-- 왼쪽: 일정 입력 -->
    <div class="left-section">
      <h2>📅 일정 입력</h2>
      <Calendar />
      <ScheduleForm @updateNotification="updateNotificationText" />
    </div>

    <!-- 가운데: 수동 알림 미리보기 -->
    <div class="middle-section">
      <h2>📢 수동 알림 미리보기</h2>
      <div class="preview-row">
        <NotificationPreview :message="notificationText" />
      </div>
      <button class="action-button" @click="sendManualNotification">📩 수동 문자 보내기</button>
    </div>

    <!-- 오른쪽: 날씨 기반 알림 -->
    <div class="right-section">
      <h2>🌤️ 날씨 기반 알림</h2>
      <div class="preview-row">
        <NotificationPreview :message="weatherNotificationText" />
      </div>
      <div v-if="changedSchedules.length" class="report-section">
        <h3>🔄 변경된 스케줄</h3>
        <table>
          <thead>
            <tr><th>날짜</th><th>시간</th><th>프로그램</th><th>야외</th><th>교사</th></tr>
          </thead>
          <tbody>
            <tr v-for="s in changedSchedules" :key="s.datefcst">
              <td>{{ formatDate(s.datefcst) }}</td>
              <td>{{ s.minutes }}</td>
              <td>{{ s.program }}</td>
              <td>{{ s.isoutside ? '예' : '아니오' }}</td>
              <td>{{ s.teacher }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <button class="action-button" @click="sendWeatherNotification">📩 날씨 문자 보내기</button>
    </div>
  </div>
</template>

<script setup>
import Calendar from "@/components/Schedule/Calendar.vue";
import ScheduleForm from "@/components/Schedule/ScheduleForm.vue";
import NotificationPreview from "@/components/notification/NotificationPreview.vue";
import api from "@/modules/axios.js";
import { onMounted, ref } from "vue";

const notificationText = ref("");
const weatherNotificationText = ref("");
const changedSchedules = ref([]);

onMounted(() => {
  fetchChangedSchedules();
});

const updateNotificationText = (message) => {
  notificationText.value = message;
};

const fetchChangedSchedules = async () => {
  try {
    const response = await api.get("/schedule/api/changed-schedules", {
      params: { nx: 62, ny: 126 },
      timeout: 30000,
    });
    changedSchedules.value = response.data.changed_schedules;
    weatherNotificationText.value = response.data.message;
  } catch (error) {
    console.error("API 호출 실패:", error);
  }
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

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString("ko-KR", {
    year: "numeric",
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

.preview-row {
  display: flex;
  align-items: center;
  width: 100%;
}

.report-section {
  margin-top: 20px;
  width: 100%;
}

table {
  width: 100%; /* 테이블 너비를 100%로 유지 */
  border-collapse: collapse;
  margin-top: 10px;
  table-layout: fixed; /* 열 너비를 고정하여 균등 분배 */
}

th, td {
  border: 1px solid #ddd;
  padding: 10px; /* 패딩을 늘려 더 넓게 보이도록 */
  text-align: left;
  word-wrap: break-word; /* 긴 텍스트가 넘어갈 경우 줄바꿈 */
}

th {
  background-color: #f2f2f2;
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
  width: 100%; /* 버튼을 섹션 너비에 맞춤 */
  text-align: center;
}
</style>