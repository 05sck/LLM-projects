<template>
  <div class="medication-page">
    <div class="chat-container">
      <!-- Jellybean Letter 로고 -->
      <h2 class="content-logo">🫘 Jellybean Letter</h2>
      <div class="content-wrapper">
        <!-- 보고서 입력 -->
        <div class="input-section">
          <p class="subtitle">✍️ <strong>보고서 입력</strong></p>
          <div class="chat-box">
            <div class="chat-message bot">
              <span>아이 이름이 무엇인가요?</span>
              <input v-model="childName" placeholder="아이 이름 입력" class="chat-input" />
            </div>
            <div class="chat-message bot">
              <span>약 이름이 무엇인가요?</span>
              <input v-model="medName" placeholder="약 이름 입력" class="chat-input" />
            </div>
            <div class="chat-message bot">
              <span>상황을 설명해주세요.</span>
              <input v-model="condition" placeholder="예: 열이 나서" class="chat-input" />
            </div>
            <div class="chat-message bot">
              <span>추가 정보를 선택해주세요 (중복 가능)</span>
              <div class="checkbox-group">
                <label><input type="checkbox" v-model="medInfo" value="효능"> 효능</label>
                <label><input type="checkbox" v-model="medInfo" value="사용법"> 사용법</label>
                <label><input type="checkbox" v-model="medInfo" value="주의사항"> 주의사항</label>
                <label><input type="checkbox" v-model="medInfo" value="상호작용"> 상호작용</label>
                <label><input type="checkbox" v-model="medInfo" value="부작용"> 부작용</label>
              </div>
            </div>
            <button class="generate-btn" @click="generateReport">📋 보고서 생성</button>
          </div>
        </div>

        <!-- 보고서 생성 결과 -->
        <div class="output-section">
          <p class="subtitle">📄 <strong>복약 보고 안내문</strong></p>
          <div class="output-box" v-if="isLoading || reportGenerated">
            <div class="output-content">
              <span v-if="isLoading || reportGenerated">
                식품의약품 안전처_의약품개요정보(e약은요)에서 {{ medName || "약 이름" }}, 
                {{ medInfo.length ? medInfo.join(", ") : "기본 정보" }}을 찾고 있습니다.
              </span>
              <div v-if="isLoading" class="loading">문서 로딩 시작...</div>
              <div v-if="processLog.length" class="log-section">
                <span>찾은 문서들입니다:</span>
                <div class="log-container">
                  <div v-for="(log, index) in processLog.slice(1, 3)" :key="index" class="log-item">
                    {{ log }}
                  </div>
                </div>
              </div>
              <!-- '복약 보고서를 생성합니다'를 별도 div로 분리 -->
              <div v-if="reportGenerated" class="report-generation">
                <span>복약 보고서를 생성합니다</span>
              </div>
              <p v-if="notificationText" class="report-text">{{ notificationText }}</p>
              <button v-if="reportGenerated" class="send-btn" @click="sendNotification">
              📩 생성된 보고서 기반으로 문자 보내기
            </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from "@/modules/axios.js";
import { ref } from "vue";

const childName = ref("");
const medName = ref("");
const condition = ref("");
const medInfo = ref([]);
const notificationText = ref("");
const processLog = ref([]);
const isLoading = ref(false);
const reportGenerated = ref(false);

const generateReport = async () => {
  if (!childName.value?.trim() || !medName.value?.trim() || !condition.value?.trim()) {
    const infoText = medInfo.value.length > 0 ? `\n추가 정보: ${medInfo.value.join(", ")}` : "";
    notificationText.value = `📋 [복약 보고서] ${childName.value || "미입력"} - ${medName.value || "미입력"}\n상황: ${condition.value || "미입력"}${infoText}`;
    processLog.value = [];
    isLoading.value = true;
    setTimeout(() => {
      isLoading.value = false;
      reportGenerated.value = true;
    }, 1000);
    return;
  }

  isLoading.value = true;
  reportGenerated.value = false;

  try {
    const params = {
      child_name: childName.value,
      med_name: medName.value,
      condition: condition.value,
      med_info: medInfo.value.join(",") || "기본 정보",
    };
    const res = await api.get("/medicine-info/", { params });
    processLog.value = res.data.process_log || [];
    notificationText.value = res.data.message || "";
  } catch (error) {
    const infoText = medInfo.value.length > 0 ? `\n추가 정보: ${medInfo.value.join(", ")}` : "";
    notificationText.value = `📋 [복약 보고서] ${childName.value} - ${medName.value}\n상황: ${condition.value}${infoText}`;
    processLog.value = [];
  }

  setTimeout(() => {
    isLoading.value = false;
    reportGenerated.value = true;
  }, 1000);
};

const sendNotification = async () => {
  if (!notificationText.value) {
    alert("⚠️ 보고서가 없습니다!");
    return;
  }
  try {
    const res = await api.post("/api/send_line", {
      child_name: childName.value,
      med_name: medName.value,
      condition: condition.value,
      med_info: medInfo.value, // 이미 배열 형태
      line_id: "Uaecc6981aace6cd3c6788ffb6019f1ff",
    });
    alert(`📩 ${res.data.message}`);
    resetForm();
  } catch (error) {
    console.error("Failed to send LINE message:", error.response ? error.response.data : error.message);
    alert("📩 LINE 전송 실패!");
  }
};

const resetForm = () => {
  childName.value = "";
  medName.value = "";
  condition.value = "";
  medInfo.value = [];
  notificationText.value = "";
  processLog.value = [];
  isLoading.value = false;
  reportGenerated.value = false;
};
</script>

<style scoped>
.medication-page {
  padding: 40px;
  background: #ffffff;
  font-family: 'Noto Sans KR', sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-container {
  max-width: 1200px;
  margin: 0 auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* Jellybean Letter 로고 스타일 */
.content-logo {
  font-family: 'Poppins', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #ff6f61, #ffb88c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-align: center;
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
}

.content-wrapper {
  display: flex;
  gap: 40px;
  flex: 1;
  margin-top: 60px; /* 로고와 겹치지 않도록 상단 여백 추가 */
  height: calc(100% - 230px); /* 로고와 여백을 고려한 높이 조정 */
}

.input-section, .output-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.subtitle {
  font-size: 1.2rem;
  color: #4a4a4a;
  margin-bottom: 20px;
}

.chat-box {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.output-box {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.output-content {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-message {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-message.bot span {
  font-size: 1.1rem;
  color: #4a4a4a;
  font-weight: 500;
}

.chat-input {
  padding: 10px;
  font-size: 1rem;
  border: 2px solid #ff6f61;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s ease;
  background: #fff;
}

.chat-input:focus {
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

.generate-btn {
  padding: 12px 20px;
  font-size: 1.1rem;
  font-weight: 600;
  background-color: #ff6f61;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
  margin-top: 20px;
}

.generate-btn:hover {
  background-color: #e65a50;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.3);
}

.loading {
  font-size: 1rem;
  color: #ff6f61;
}

.log-section {
  margin-top: 10px;
}

.log-container {
  display: flex;
  gap: 15px;
  margin-top: 10px;
  height: 100px;
}

.log-item {
  flex: 1;
  padding: 10px;
  background: #ffffff;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #333;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  height: 100%;
}

.report-text {
  font-size: 1.1rem;
  color: #333;
  white-space: pre-wrap;
}

.report-generation {
  margin-top: 15px;
  font-size: 1rem;
  color: #ff6f61;
  font-weight: 500;
}

.send-btn {
  padding: 12px 20px;
  font-size: 1.1rem;
  font-weight: 500;
  background-color: #ff6f61;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.send-btn:hover {
  background-color: #e65a50;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(255, 111, 97, 0.3);
}

@media (max-width: 768px) {
  .medication-page {
    padding: 20px;
  }

  .content-logo {
    font-size: 2rem;
    top: -30px;
  }

  .content-wrapper {
    flex-direction: column;
    margin-top: 40px; /* 모바일에서 조정 */
    height: calc(100% - 200px); /* 모바일에서 높이 조정 */
  }

  .chat-input {
    font-size: 0.9rem;
  }

  .generate-btn, .send-btn {
    font-size: 1rem;
    padding: 10px 15px;
  }
}
</style>