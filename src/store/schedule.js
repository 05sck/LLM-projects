import { defineStore } from "pinia";

export const useScheduleStore = defineStore("schedule", {
  state: () => ({
    events: [],
  }),
  actions: {
    async fetchEvents() {
      try {
        // API 요청이 없을 경우, 더미 데이터 사용
        this.events = [
          { id: 1, event_name: "소풍", event_date: "2025-03-25" },
          { id: 2, event_name: "체육대회", event_date: "2025-04-10" }
        ];
      } catch (error) {
        console.error("일정 데이터를 불러오는 중 오류 발생:", error);
      }
    },
    async addEvent(event) {
      try {
        this.events.push({
          id: this.events.length + 1,
          event_name: event.event_name,
          event_date: event.event_date,
          reason: event.reason
        });
      } catch (error) {
        console.error("일정 추가 중 오류 발생:", error);
      }
    }
  },
});
