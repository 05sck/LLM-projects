<template>
  <div class="schedule-form">
    <label>📌 일정명</label>
    <input type="text" v-model="eventName" placeholder="일정명을 입력하세요" />
  
      <label>📆 변경 날짜</label>
      <input type="date" v-model="newDate" />
  
      <label>📝 변경 사유</label>
      <textarea v-model="reason"></textarea>
  
      <button @click="generateNotification">🔔 알림 미리보기</button>
    </div>
  </template>
  
  <script setup>
  import axios from '@/modules/axios.js'; // 객체로 가져옴
import { defineEmits, ref } from "vue";
  
  const emit = defineEmits(["updateNotification"]);
  
  const eventName = ref("");
  const newDate = ref("");
  const reason = ref("");
  
  const generateNotification = async () => {
  console.log("버튼 클릭됨");  // 버튼 동작 확인
  try {
    console.log("요청 시작:", {
      event: eventName.value,
      date: newDate.value,
      reason: reason.value
    });
    const response = await axios.post('/schedule/api/send-message', {
      event: eventName.value,
      date: newDate.value,
      reason: reason.value
    });
    console.log("응답 수신:", response.data);
    const generatedMessage = response.data.message;
    emit("updateNotification", generatedMessage);
  } catch (error) {
    console.error("요청 오류:", error.message);
    emit("updateNotification", `오류 발생: ${error.message}`);
  }
};
</script>
  
  <style scoped>
  .schedule-form {
    text-align: left;
  }
  
  label {
    display: block;
    margin-top: 10px;
    font-weight: bold;
  }
  
  input, select, textarea {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
  }
  
  button {
    margin-top: 15px;
    background-color: #007bff;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>
  