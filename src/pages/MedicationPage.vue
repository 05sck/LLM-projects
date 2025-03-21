<template>
  <div class="medication-page">
    <div class="input-section">
      <h1>💊 복약 정보</h1>
      <MedicationTable />
      <MedicationForm @updateNotification="updateNotificationText" />
    </div>
    <div class="output-section">
      <h2>📢 알림 미리보기</h2>
      <NotificationPreview :message="notificationText" />
      <div class="buttons">
        <button class="send-btn" @click="sendNotification">📩 문자 보내기</button>
        <button class="reset-btn" @click="resetForm">🔄 입력 초기화</button>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import MedicationForm from "@/components/medication/MedicationForm.vue";
import MedicationTable from "@/components/medication/MedicationTable.vue";
import NotificationPreview from "@/components/notification/NotificationPreview.vue";
import api from "@/modules/axios.js";
import { ref } from "vue";
  
const notificationText = ref("");

const updateNotificationText = (message) => {
    notificationText.value = message;
  };

  const sendNotification = async () => {
  if (!notificationText.value) {
    alert("⚠️ 알림 문자가 없습니다! 먼저 '알림 생성'을 눌러주세요.");
    return;
  }
  try {
    console.log("Sending to /api/send_line:", notificationText.value);  // 디버깅
    const res = await api.post("/api/send_line", {
      message: notificationText.value,
      user_id: "Uaecc6981aace6cd3c6788ffb6019f1ff",  // 동일한 사용자 ID
    });
    console.log("Response:", res.data);
    alert(`📩 ${res.data.message}`);
    notificationText.value = "";
  } catch (error) {
    console.error("Failed to send LINE message:", error.response ? error.response.data : error.message);
    alert("📩 LINE 전송 실패!");
  }
};
  
  const resetForm = () => {
    notificationText.value = "";
  };
  </script>
  
  <style scoped>
  .medication-page {
    display: flex;
    justify-content: space-between;
    padding: 20px;
  }
  
  .input-section {
    width: 45%;
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
  }
  
  .output-section {
    width: 50%;
    background: #ffffff;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
  }
  
  .notification-container {
    min-height: 100px;
  }
  
  .buttons {
    margin-top: 20px;
  }
  
  button {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .send-btn {
    background-color: #007bff;
    color: white;
  }
  
  .reset-btn {
    background-color: #28a745;
    color: white;
  }
  </style>
  