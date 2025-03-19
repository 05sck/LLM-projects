<template>
  <div>
    <h1>💊 복약 정보</h1>

    <label>아이 이름</label>
    <input v-model="childName" />

    <label>약 이름</label>
    <input v-model="medicine" />

    <label>용량</label>
    <input type="number" v-model="dosage" />

    <label>증상</label>
    <textarea v-model="symptoms"></textarea>

    <button @click="saveMedication">저장 및 알림</button>

    <h2>📋 복약 기록</h2>
    <button @click="fetchRecords">📋 복약 기록 불러오기</button>
    <ul>
      <li v-for="record in records" :key="record.id">
        {{ record.child_name }} - {{ record.medicine }} ({{ record.dosage }}ml)
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "@/services/api";

const childName = ref("");
const medicine = ref("");
const dosage = ref("");
const symptoms = ref("");
const records = ref([]);

const fetchRecords = async () => {
  try {
    const response = await api.get("/medication");
    records.value = response.data;
  } catch (error) {
    console.error("복약 기록 불러오기 실패:", error);
  }
};

const saveMedication = async () => {
  try {
    await api.post("/medication", {
      child_name: childName.value,
      medicine: medicine.value,
      dosage: dosage.value,
      symptoms: symptoms.value,
    });
    fetchRecords();
  } catch (error) {
    console.error("복약 기록 추가 실패:", error);
  }
};
</script>
