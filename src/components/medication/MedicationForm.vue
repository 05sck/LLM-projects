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
import { defineEmits, ref } from "vue";

const emit = defineEmits(["update-notification"]);

const childName = ref("");
const medName = ref("");
const condition = ref("");
const medInfo = ref([]);

async function submitForm() {
  if (!childName.value?.trim() || !medName.value?.trim() || !condition.value?.trim()) {
    console.error("아이 이름, 약 이름, 상황 설명을 모두 입력해주세요");
    const infoText = medInfo.value.length > 0 ? `\n약 정보: ${medInfo.value.join(", ")}` : "";
    const fallbackMessage = `📢 [유치원 복약 안내] ${childName.value || "미입력"} - ${medName.value || "미입력"}\n상황: ${condition.value || "미입력"}${infoText}`;
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
    console.log("전송 파라미터:", params);
    const res = await api.get("/medicine-info/", { params });
    console.log("RAG 응답:", res.data);
    emit("update-notification", {
      message: res.data.message,
      process_log: res.data.process_log
    });
  } catch (error) {
    console.error("약 정보 조회 실패:", error.response ? error.response.data : error);
    const infoText = medInfo.value.length > 0 ? `\n약 정보: ${medInfo.value.join(", ")}` : "";
    const fallbackMessage = `📢 [유치원 복약 안내] ${childName.value} - ${medName.value}\n상황: ${condition.value}${infoText}`;
    emit("update-notification", { message: fallbackMessage, process_log: [] });
  }
}
</script>

<style scoped>
.medication-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  font-family: 'Noto Sans KR', sans-serif;
}

h2 {
  font-size: 1.5rem;
  color: #4a4a4a;
  margin-bottom: 10px;
}

label {
  font-size: 1.1rem;
  color: #4a4a4a;
  font-weight: 500;
}

input[type="text"] {
  padding: 10px;
  font-size: 1rem;
  border: 2px solid #ff6f61;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s ease;
}

input[type="text"]:focus {
  border-color: #e65a50;
  box-shadow: 0 0 5px rgba(255, 111, 97, 0.5);
}

.med-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.med-info label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  color: #4a4a4a;
}

.med-info input[type="checkbox"] {
  accent-color: #ff6f61; /* 체크박스 색상 */
  width: 16px;
  height: 16px;
}

button {
  padding: 10px 20px;
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
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.3);
}

@media (max-width: 768px) {
  .medication-form {
    gap: 10px;
  }

  h2 {
    font-size: 1.3rem;
  }

  input[type="text"],
  button {
    font-size: 0.9rem;
  }
}
</style>