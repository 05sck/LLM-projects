<template>
    <div class="medication-table">
      <h2>💊 유치원 보유 약 목록</h2>
      <table>
        <thead>
          <tr>
            <th>약 이름</th>
            <th>증상</th>
            <th>주의사항</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(medicine, index) in medicines" :key="index">
            <td>{{ medicine.name }}</td>
            <td>{{ medicine.symptom }}</td>
            <td>{{ medicine.warning }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const medicines = ref([
    { name: "타이레놀", symptom: "두통", warning: "공복 복용 금지" },
    { name: "센트룸", symptom: "비타민 보충", warning: "과다 복용 주의" },
    { name: "알러지약", symptom: "가려움증", warning: "졸림 유발 가능" },
  ]);
  </script>
  
  <style scoped>
  .medication-table {
    margin-bottom: 20px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  </style>
  