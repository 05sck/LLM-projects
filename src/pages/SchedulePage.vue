<template>
  <div class="schedule-page">
    <!-- 좌측 입력 부분 -->
    <div class="input-section">
      <Calendar />
      <ScheduleForm @updateNotification="updateNotificationText" />
    </div>

    <!-- 우측 출력 부분 -->
    <div class="output-section">
      <h2>📢 알림 미리보기</h2>
      <NotificationPreview :message="notificationText" />
      <div class="buttons">
        <button @click="sendNotification">📩 문자 보내기</button>
        <button @click="updateCalendar">📆 캘린더 일정 변경하기</button>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import Calendar from "@/components/Schedule/Calendar.vue";
import ScheduleForm from "@/components/Schedule/ScheduleForm.vue";
import NotificationPreview from "@/components/notification/NotificationPreview.vue";
import api from "@/modules/axios.js";
import { ref } from "vue";
  
const notificationText = ref("");

// 🔹 일정 변경 시 알림 문자 업데이트
const updateNotificationText = (message) => {
  notificationText.value = message;
};

// 🔹 문자 전송
const sendNotification = async () => {
  if (!notificationText.value) {
    alert("⚠️ 알림 메시지가 없습니다! 먼저 '알림 미리보기'를 생성해주세요.");
    return;
  }
  try {
    console.log("Requesting /api/send_line with:", {
      message: notificationText.value,
      user_id: "Uaecc6981aace6cd3c6788ffb6019f1ff",
    });
    const res = await api.post("/api/send_line", {
      message: notificationText.value,
      user_id: "Uaecc6981aace6cd3c6788ffb6019f1ff",
    });
    console.log("Response:", res.data);  // 성공 응답 확인
    alert(`📩 ${res.data.message}`);
    notificationText.value = "";
  } catch (error) {
    console.error("Failed to send LINE message:", error.response ? error.response.data : error.message);
    alert("📩 LINE 전송 실패!");
  }
};

// 🔹 캘린더 일정 업데이트
const updateCalendar = () => {
  alert("📆 캘린더 일정이 변경되었습니다!");
};
</script>
  
<style scoped>
.schedule-page {
  display: flex;
  width: 90%;
  margin: 20px auto;
  gap: 20px; /* 좌우 간격 */
  min-height: 100vh; /* ✅ 유동적인 높이 적용 */
}

.input-section {
  flex: 1; /* 좌측 일정 입력 부분 */
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.output-section {
  flex: 1; /* 우측 알림 미리보기 */
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

button {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:first-child {
  background-color: #007bff;
  color: white;
}

button:last-child {
  background-color: #28a745;
  color: white;
}
</style>
