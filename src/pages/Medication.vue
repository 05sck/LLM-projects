<template>
    <div>
      <h1>💊 복약 정보</h1>
      
      <label>아이 이름</label>
      <input v-model="childName" />
      
      <label>몸무게</label>
      <input type="number" v-model="childWeight" />
      
      <label>약 이름</label>
      <input v-model="medicine" />
      
      <label>용량</label>
      <input type="number" v-model="dosage" />
      
      <label>증상</label>
      <textarea v-model="symptoms"></textarea>
      
      <button @click="saveMedication">저장 및 알림</button>
  
      <h2>📋 복약 기록</h2>
      <ul>
        <li v-for="record in medicationStore.records" :key="record.id">
          {{ record.child_name }} - {{ record.medicine }} ({{ record.dosage }}ml)
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useMedicationStore } from "@/store/medication";
  
  const childName = ref("");
  const childWeight = ref("");
  const medicine = ref("");
  const dosage = ref("");
  const symptoms = ref("");
  const medicationStore = useMedicationStore();
  
  const saveMedication = () => {
    medicationStore.addRecord({
      child_name: childName.value,
      weight: childWeight.value,
      medicine: medicine.value,
      dosage: dosage.value,
      symptoms: symptoms.value,
    });
  };
  
  onMounted(() => {
    medicationStore.fetchRecords();
  });
  </script>
  