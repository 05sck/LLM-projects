<template>
  <div class="medication-page">
    <!-- 좌측: 입력 폼 -->
    <div class="input-section">
      <h1>💊 복약 정보</h1>
      <MedicationTable />
      <MedicationForm @updateNotification="updateNotificationText" />
    </div>

    <!-- 우측: 알림 미리보기 -->
    <div class="output-section">
      <h2>📢 알림 미리보기</h2>
      <div class="notification-container">
        <NotificationPreview :message="notificationText" />
      </div>
      
      <div class="buttons">
        <button class="send-btn" @click="sendNotification">📩 문자 보내기</button>
        <button class="reset-btn" @click="resetForm">🔄 입력 초기화</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import MedicationTable from "@/components/MedicationTable.vue";
import MedicationForm from "@/components/MedicationForm.vue";
import NotificationPreview from "@/components/NotificationPreview.vue";

const notificationText = ref("");  // 알림 문구

// 🔥 알림 업데이트 함수
const updateNotificationText = (message) => {
  notificationText.value = message;
};

// 📩 문자 전송 기능
const sendNotification = () => {
  if (notificationText.value.trim() === "") {
    alert("⚠️ 알림 문자가 없습니다!");
    return;
  }
  alert("📩 문자 전송 완료!");
};

// 🔄 입력 데이터 초기화
const resetForm = () => {
  notificationText.value = "";  // 알림 초기화
};
</script>

<style scoped>
/* 🔹 기본 컨테이너 스타일 */
.medication-page {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 20px;
}

/* 🔹 좌측 입력 폼 */
.input-section {
  width: 50%;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  overflow-y: auto; /* 🔥 높이 초과 시 스크롤 */
  max-height: 600px;
}

/* 🔹 우측 알림 미리보기 */
.output-section {
  width: 50%;
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

/* 🔹 알림 미리보기 자동 확장 */
.notification-container {
  min-height: 100px;
  max-height: 300px;
  overflow-y: auto;
  background: #f3f3f3;
  padding: 10px;
  border-radius: 5px;
}

/* 🔹 버튼 스타일 */
.buttons {
  margin-top: 20px;
}

button {
  margin: 10px;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

.send-btn {
  background-color: #007bff;
  color: white;
}

.reset-btn {
  background-color: #dc3545;
  color: white;
}

button:hover {
  opacity: 0.8;
}
</style>
