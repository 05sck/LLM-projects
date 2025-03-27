<template>
  <div class="medication-form">
    <h2 class="form-title">📝 보고서 입력</h2>
    <div class="form-group">
      <label>아이 이름</label>
      <input v-model="childName" placeholder="아이 이름 입력" />
    </div>
    <div class="form-group">
      <label>약 이름</label>
      <input v-model="medName" placeholder="약 이름 입력" />
    </div>
    <div class="form-group">
      <label>상황 설명</label>
      <input v-model="condition" placeholder="예: 열이 나서" />
    </div>
    <div class="form-group">
      <label>추가 정보 (선택)</label>
      <div class="checkbox-group">
        <label><input type="checkbox" v-model="medInfo" value="효능"> 효능</label>
        <label><input type="checkbox" v-model="medInfo" value="사용법"> 사용법</label>
        <label><input type="checkbox" v-model="medInfo" value="주의사항"> 주의사항</label>
        <label><input type="checkbox" v-model="medInfo" value="상호작용"> 상호작용</label>
        <label><input type="checkbox" v-model="medInfo" value="부작용"> 부작용</label>
      </div>
    </div>
    <button @click="submitForm">📋 보고서 생성</button>
  </div>
</template>

<script setup>
import api from "@/modules/axios.js";
import { defineEmits, ref } from "vue";

const emit = defineEmits(["update-notification"]);

const childName = ref("");
const medName = ref("");
const condition = ref("");
const medInfo = ref([]);

async function submitForm() {
  if (!childName.value?.trim() || !medName.value?.trim() || !condition.value?.trim()) {
    const infoText = medInfo.value.length > 0 ? `\n추가 정보: ${medInfo.value.join(", ")}` : "";
    const fallbackMessage = `📋 [복약 보고서] ${childName.value || "미입력"} - ${medName.value || "미입력"}\n상황: ${condition.value || "미입력"}${infoText}`;
    emit("update-notification", { message: fallbackMessage, process_log: [] });
    return;
  }

  try {
    const params = {
      child_name: childName.value,
      med_name: medName.value,
      condition: condition.value,
      med_info: medInfo.value.join(",") || "기본 정보",
    };
    const res = await api.get("/medicine-info/", { params });
    emit("update-notification", {
      message: res.data.message,
      process_log: res.data.process_log,
    });
  } catch (error) {
    const infoText = medInfo.value.length > 0 ? `\n추가 정보: ${medInfo.value.join(", ")}` : "";
    const fallbackMessage = `📋 [복약 보고서] ${childName.value} - ${medName.value}\n상황: ${condition.value}${infoText}`;
    emit("update-notification", { message: fallbackMessage, process_log: [] });
  }
}
</script>

<style scoped>
.medication-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-title {
  font-size: 1.5rem;
  color: #4a4a4a;
  font-weight: 600;
  margin-bottom: 10px;
}

.form-group label {
  font-size: 1.1rem;
  color: #4a4a4a;
  font-weight: 500;
  display: block;
  margin-bottom: 5px;
}

.form-group input[type="text"] {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
  border: 2px solid #ff6f61;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s ease;
  background: #fff;
}

.form-group input[type="text"]:focus {
  border-color: #e65a50;
  box-shadow: 0 0 8px rgba(255, 111, 97, 0.3);
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  color: #4a4a4a;
}

.checkbox-group input[type="checkbox"] {
  accent-color: #ff6f61;
  width: 18px;
  height: 18px;
}

button {
  padding: 12px 20px;
  font-size: 1.1rem;
  font-weight: 600;
  background-color: #ff6f61;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #e65a50;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.3);
}
</style>