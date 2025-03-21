<template>
  <div class="medication-form">
    <h2>📝 복약 정보 입력</h2>

    <label>아이 이름</label>
    <input v-model="childName" placeholder="아이 이름 입력" />

    <label>약 이름</label>
    <input v-model="medName" placeholder="약 이름 입력" />

    <label>상황 설명</label>
    <input v-model="condition" placeholder="예: 열이 나서" />

    <label>약 정보 (중복 선택 가능)</label>
    <div class="med-info">
      <label><input type="checkbox" v-model="medInfo" value="효능"> 효능</label>
      <label><input type="checkbox" v-model="medInfo" value="사용법"> 사용법</label>
      <label><input type="checkbox" v-model="medInfo" value="주의사항"> 주의사항</label>
      <label><input type="checkbox" v-model="medInfo" value="상호작용"> 상호작용</label>
      <label><input type="checkbox" v-model="medInfo" value="부작용"> 부작용</label>
    </div>

    <button @click="submitForm">알림 생성</button>
  </div>
</template>
  
<script setup>
import api from "@/modules/axios.js";
import { defineEmits, onMounted, ref } from "vue";

const emit = defineEmits(["updateNotification", "submit"]);

const childName = ref("");  // 아이 이름 직접 입력
const medName = ref("");    // 약 이름 직접 입력
const condition = ref("");
const medInfo = ref([]); //약 정보 배열로 중복

onMounted(async () => {
  try {
    const childRes = await api.get("/api/children");
    children.value = childRes.data.children || [];
    const medRes = await api.get("/api/medications");
    medications.value = medRes.data.medications || [];
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
});

// 📢 알림 생성
function submitForm() {
  if (!childName.value || !medName.value) {
    console.error("아이 이름과 약 이름을 입력해주세요");
    return;
  }
  const infoText = medInfo.value.length > 0 ? `\n약 정보: ${medInfo.value.join(", ")}` : "";
  const message = `📢 [유치원 복약 안내] ${childName.value} - ${medName.value}\n상황: ${condition.value}${infoText}`;
  emit("updateNotification", message);
}
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
  