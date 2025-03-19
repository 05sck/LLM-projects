<template>
  <div class="schedule-page">
    <div class="form-container">
      <label>일정명</label>
      <select v-model="eventName">
        <option v-for="option in mockEvents" :key="option.id" :value="option.name">
          {{ option.name }}
        </option>
      </select>

      <label>변경할 날짜</label>
      <input type="date" v-model="eventDate" />

      <label>변경 사유</label>
      <textarea v-model="reason"></textarea>

      <button @click="saveEvent">저장 및 알림 전송</button>
    </div>

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

// ✅ 목업 데이터 (실제 API 대신 사용)
const mockEvents = [
  { id: 1, name: "소풍", date: "2025-03-20" },
  { id: 2, name: "체육대회", date: "2025-03-22" }
];

const eventName = ref(mockEvents[0].name); // 기본 선택값
const eventDate = ref("");
const reason = ref("");
const events = ref([]);

// ✅ API 요청 중복 방지
const isFetching = ref(false);

// ✅ API가 없을 경우 목업 데이터 사용
const useMockData = true;

// ✅ 일정 목록 가져오기
const fetchEvents = async () => {
  if (isFetching.value) return;
  isFetching.value = true;

  try {
    console.log("📡 일정 목록 API 요청...");
    await new Promise((resolve) => setTimeout(resolve, 500));

    if (useMockData) {
      events.value = mockEvents; // 🔥 목업 데이터 사용
    } else {
      const response = await api.get("/schedule");
      events.value = response.data;
    }
    console.log("✅ 일정 목록 불러오기 성공:", events.value);
  } catch (error) {
    console.error("❌ 일정 목록 불러오기 실패:", error);
  } finally {
    isFetching.value = false;
  }
};

// ✅ 일정 저장
const saveEvent = async () => {
  try {
    console.log("📡 일정 추가 요청:", eventName.value, eventDate.value);

    if (useMockData) {
      // 🔥 목업 데이터에 일정 추가
      mockEvents.push({ id: mockEvents.length + 1, name: eventName.value, date: eventDate.value });
      fetchEvents(); // 바로 갱신
      return;
    }

    await api.post("/schedule", {
      event_name: eventName.value,
      event_date: eventDate.value,
      reason: reason.value,
    });

    await fetchEvents(); // ✅ 저장 후 목록 갱신
  } catch (error) {
    console.error("❌ 일정 추가 실패:", error);
  }
};

// ✅ 페이지 로드 시 일정 목록 불러오기
onMounted(fetchEvents);
</script>

<style scoped>
.schedule-page {
  padding: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

button {
  background: #42b983;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #369f6f;
}
</style>
