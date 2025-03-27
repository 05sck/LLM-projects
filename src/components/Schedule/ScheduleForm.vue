<template>
  <div class="schedule-form">
    <label>📌 일정명</label>
    <input type="text" v-model="eventName" placeholder="일정명" />

    <label>📆 변경 날짜</label>
    <input type="date" v-model="newDate" />

    <label>📝 변경 사유</label>
    <textarea v-model="reason" placeholder="사유"></textarea>

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
  padding: 10px; /* 전체 패딩 줄임 */
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); /* Home.vue와 유사한 배경 */
  border-radius: 8px; /* 둥근 모서리 추가 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05); /* 약간의 그림자 */
  max-width: 300px; /* 폭 제한으로 컴팩트하게 */
}

label {
  display: block;
  margin-top: 5px; /* 마진 최소화 */
  font-weight: bold;
  font-size: 0.9rem; /* 글씨 크기 줄임 */
  color: #4a4a4a; /* Home.vue와 색상 통일 */
}

input, textarea {
  width: 100%;
  padding: 5px; /* 패딩 줄여서 높이 최소화 */
  margin-top: 2px; /* 마진 줄임 */
  font-size: 0.9rem; /* 글씨 크기 줄임 */
  border: 1px solid #e0e0e0; /* 경계선 추가 */
  border-radius: 4px; /* 둥근 모서리 */
  box-sizing: border-box; /* 패딩 포함 폭 계산 */
}

textarea {
  height: 40px; /* 텍스트 영역 높이 대폭 줄임 */
  resize: none; /* 크기 조정 비활성화 */
}

button {
  margin-top: 8px; /* 마진 줄임 */
  background-color: #ff6f61; /* Home.vue와 색상 통일 */
  color: white;
  padding: 6px 12px; /* 버튼 크기 줄임 */
  border: none;
  border-radius: 4px; /* 둥근 모서리 */
  cursor: pointer;
  font-size: 0.9rem; /* 글씨 크기 줄임 */
  transition: background-color 0.3s ease; /* 호버 효과 */
}

button:hover {
  background-color: #e65a50; /* Home.vue와 유사한 호버 색상 */
}
</style>