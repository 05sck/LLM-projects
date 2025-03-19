<template>
    <div class="medication-form">
      <h2>📝 복약 정보 입력</h2>
  
      <label>아이 이름</label>
      <input v-model="childName" placeholder="아이 이름 입력" />
  
      <label>아이 나이</label>
      <input type="number" v-model="childAge" placeholder="나이 입력" />
  
      <label>아이 몸무게</label>
      <input type="number" v-model="childWeight" placeholder="몸무게 입력 (kg)" />
  
      <label>약 이름</label>
      <input v-model="medicineName" placeholder="복용할 약 입력" />
  
      <label>복용량</label>
      <input type="number" v-model="dosage" placeholder="복용량 입력 (ml)" />
  
      <label>복용 시간</label>
      <input type="time" v-model="time" />
  
      <button @click="generateNotification">알림 미리보기</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const emit = defineEmits(["updateNotification"]);
  
  const childName = ref("");
  const childAge = ref("");
  const childWeight = ref("");
  const medicineName = ref("");
  const dosage = ref("");
  const time = ref("");
  
  // 📢 알림 생성
  const generateNotification = () => {
    const message = `📢 [유치원 복약 안내] ${childName.value}(${childAge.value}세, ${childWeight.value}kg) 
    ${medicineName.value} ${dosage.value}ml 복용 예정 - 시간: ${time.value}`;
  
    emit("updateNotification", message);
  };
  </script>
  
  <style scoped>
  .medication-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  input, button {
    padding: 8px;
    font-size: 16px;
  }
  
  button {
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    opacity: 0.8;
  }
  </style>
  