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
    emit("update-notification", fallbackMessage);
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
    // URL 수동 생성 및 로그 출력
    const url = new URL("http://127.0.0.1:8000/medicine-info/");
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    console.log("생성된 요청 URL:", url.toString());
    const res = await api.get("/medicine-info/", { params });
    console.log("실제 요청 URL:", res.request.responseURL);
    console.log("RAG 응답:", res.data.response);
    const response = res.data.response;
    emit("update-notification", response);
  } catch (error) {
    console.error("약 정보 조회 실패:", error.response ? error.response.data : error);
    if (error.response) {
      console.error("상세 오류:", error.response.data.detail);
      console.error("실제 요청 URL (에러 시):", error.config.url + '?' + new URLSearchParams(error.config.params).toString());
    }
    const infoText = medInfo.value.length > 0 ? `\n약 정보: ${medInfo.value.join(", ")}` : "";
    const fallbackMessage = `📢 [유치원 복약 안내] ${childName.value} - ${medName.value}\n상황: ${condition.value}${infoText}`;
    emit("update-notification", fallbackMessage);
  }
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
  