import { defineStore } from "pinia";

export const useMedicationStore = defineStore("medication", {
  state: () => ({
    records: [],
  }),
  actions: {
    async fetchRecords() {
      try {
        // 더미 데이터 추가
        this.records = [
          { id: 1, child_name: "김철수", medicine: "타이레놀", dosage: "5ml" },
          { id: 2, child_name: "이영희", medicine: "알레르기약", dosage: "2ml" },
        ];
      } catch (error) {
        console.error("복약 기록을 불러오는 중 오류 발생:", error);
      }
    },
    async addRecord(record) {
      try {
        this.records.push({
          id: this.records.length + 1,
          child_name: record.child_name,
          medicine: record.medicine,
          dosage: record.dosage,
          symptoms: record.symptoms,
        });
      } catch (error) {
        console.error("복약 기록 추가 중 오류 발생:", error);
      }
    }
  },
});
