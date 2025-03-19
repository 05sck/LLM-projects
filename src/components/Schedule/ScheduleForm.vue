<template>
    <div class="schedule-form">
      <label>📌 일정명</label>
      <select v-model="selectedEvent">
        <option v-for="event in events" :key="event.id" :value="event.name">
          {{ event.name }}
        </option>
      </select>
  
      <label>📆 변경 날짜</label>
      <input type="date" v-model="newDate" />
  
      <label>📝 변경 사유</label>
      <textarea v-model="reason"></textarea>
  
      <button @click="generateNotification">🔔 알림 미리보기</button>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from "vue";
  
  const emit = defineEmits(["updateNotification"]);
  
  const events = ref([
    { id: 1, name: "소풍" },
    { id: 2, name: "체육대회" },
    { id: 3, name: "학부모 상담" }
  ]);
  
  const selectedEvent = ref("");
  const newDate = ref("");
  const reason = ref("");
  
  const generateNotification = () => {
    const message = `📢 [유치원 일정 변경 안내]\n"${selectedEvent.value}" 일정이 ${newDate.value}로 변경되었습니다.\n사유: ${reason.value}`;
    emit("updateNotification", message);
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
  