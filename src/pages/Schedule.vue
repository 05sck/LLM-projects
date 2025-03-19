<template>
  <div>
    <h1>📅 일정 변경</h1>

    <label>일정명</label>
    <input v-model="eventName" placeholder="소풍" />

    <label>변경할 날짜</label>
    <input type="date" v-model="eventDate" />

    <label>변경 사유</label>
    <textarea v-model="reason"></textarea>

    <button @click="saveEvent">저장 및 알림 전송</button>

    <h2>📋 일정 목록</h2>
    <button @click="fetchEvents">📋 일정 목록 불러오기</button>
    <ul>
      <li v-for="event in events" :key="event.id">
        {{ event.event_name }} - {{ event.event_date }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";

const eventName = ref("");
const eventDate = ref("");
const reason = ref("");
const events = ref([]);
const isFetching = ref(false); // ✅ API 중복 요청 방지

// ✅ API 호출 함수 (429 방지 - 요청 간격 조정)
const fetchEvents = async () => {
  if (isFetching.value) return; // ✅ API 요청 중이면 새로운 요청 차단
  isFetching.value = true;

  try {
    console.log("📡 일정 목록 API 요청...");
    await new Promise((resolve) => setTimeout(resolve, 500)); // 🔥 500ms 대기 후 요청
    const response = await api.get("/schedule");
    events.value = response.data;
    console.log("✅ 일정 목록 불러오기 성공:", response.data);
  } catch (error) {
    console.error("❌ 일정 목록 불러오기 실패:", error);
  } finally {
    isFetching.value = false; // ✅ 요청이 끝난 후 다시 요청 가능하도록 변경
  }
};

// ✅ 페이지 로드 시 API 호출 (중복 요청 방지)
onMounted(async () => {
  if (events.value.length === 0) {  // ✅ 기존 데이터가 없을 때만 요청
    await fetchEvents();
  }
});

// ✅ 일정 저장 함수
const saveEvent = async () => {
  try {
    console.log("📡 일정 추가 API 요청:", eventName.value, eventDate.value);
    await api.post("/schedule", {
      event_name: eventName.value,
      event_date: eventDate.value,
      reason: reason.value,
    });
    await fetchEvents();  // ✅ 저장 후 목록 갱신
  } catch (error) {
    console.error("❌ 일정 추가 실패:", error);
  }
};
</script>
