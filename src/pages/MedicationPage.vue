<template>
  <div class="medication-page">
    <div class="input-section">
      <h1>💊 복약 정보</h1>
      <MedicationTable />
      <MedicationForm @update-notification="updateNotificationText" />
    </div>
    <div class="output-section">
      <h2>📢 알림 미리보기</h2>
      <NotificationPreview :message="notificationText" :process-log="processLog" />
      <div class="buttons">
        <button class="send-btn" @click="sendNotification">📩 문자 보내기</button>
        <button class="reset-btn" @click="resetForm">🔄 입력 초기화</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import MedicationForm from "@/components/medication/MedicationForm.vue";
import MedicationTable from "@/components/medication/MedicationTable.vue";
import NotificationPreview from "@/components/notification/NotificationPreview.vue";
import api from "@/modules/axios.js";
import { ref } from "vue";

const notificationText = ref("");
const processLog = ref([]);
let latestFormData = null;  // MedicationForm 데이터를 저장

// MedicationForm에서 받은 데이터로 미리보기 업데이트
const updateNotificationText = (data) => {
  latestFormData = {
    child_name: data.child_name,
    med_name: data.med_name,
    condition: data.condition,
    med_info: data.med_info
  };  // LINE 전송용 데이터 저장
  notificationText.value = data.message;
  processLog.value = data.process_log;
};

// LINE으로 메시지 전송
const sendNotification = async () => {
  if (!notificationText.value || !latestFormData) {
    alert("⚠️ 알림 문자가 없습니다! 먼저 '알림 생성'을 눌러주세요.");
    return;
  }
  try {
    const res = await api.post("/api/send_line", {
      child_name: latestFormData.child_name,
      med_name: latestFormData.med_name,
      condition: latestFormData.condition,
      med_info: latestFormData.med_info,
      line_id: "Uaecc6981aace6cd3c6788ffb6019f1ff"  // 고정된 LINE ID
    });
    console.log("Response:", res.data);
    alert(`📩 ${res.data.line_status}`);
    resetForm();  // 전송 후 초기화
  } catch (error) {
    console.error("Failed to send LINE message:", error.response ? error.response.data : error.message);
    alert("📩 LINE 전송 실패!");
  }
};

// 폼 초기화
const resetForm = () => {
  notificationText.value = "";
  processLog.value = [];
  latestFormData = null;
};
</script>

<style scoped>
/* 기존 스타일 유지 */
</style>

<style scoped>
.medication-page {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.input-section {
  width: 45%;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}

.output-section {
  width: 50%;
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.buttons {
  margin-top: 20px;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.send-btn {
  background-color: #007bff;
  color: white;
}

.reset-btn {
  background-color: #28a745;
  color: white;
}
</style>