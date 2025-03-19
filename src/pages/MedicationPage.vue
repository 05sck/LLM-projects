<template>
    <div class="medication-page">
      <div class="input-section">
        <h1>💊 복약 정보</h1>
        <MedicationTable />
        <MedicationForm @updateNotification="updateNotificationText" />
      </div>
  
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
  
  const notificationText = ref("");
  
  const updateNotificationText = (message) => {
    notificationText.value = message;
  };
  
  const sendNotification = () => {
    if (notificationText.value.trim() === "") {
      alert("⚠️ 알림 문자가 없습니다!");
      return;
    }
    alert("📩 문자 전송 완료!");
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
  