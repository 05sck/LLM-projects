<template>
    <div class="schedule-page">
      <!-- 좌측 입력 부분 -->
      <div class="input-section">
        <Calendar />
        <ScheduleForm @updateNotification="updateNotificationText" />
      </div>
  
      <!-- 우측 출력 부분 -->
      <div class="output-section">
        <NotificationPreview :message="notificationText" />
        <div class="buttons">
          <button @click="sendNotification">📩 문자 보내기</button>
          <button @click="updateCalendar">📆 캘린더 일정 변경하기</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import Calendar from "@/components/Calendar.vue";
  import ScheduleForm from "@/components/ScheduleForm.vue";
  import NotificationPreview from "@/components/NotificationPreview.vue";
  
  const notificationText = ref("");
  
  // ✨ 좌측 일정 입력 데이터를 받아서 알림 문자 업데이트
  const updateNotificationText = (message) => {
    notificationText.value = message;
  };
  
  // 📩 문자 전송
  const sendNotification = () => {
    alert("📩 문자 전송 완료!");
  };
  
  // 📆 캘린더 업데이트
  const updateCalendar = () => {
    alert("📆 캘린더 일정이 변경되었습니다!");
  };
  </script>
  
  <style scoped>
  .schedule-page {
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
  
  .buttons {
    margin-top: 20px;
  }
  
  button {
    margin: 10px;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
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
  