<template>
  <div class="notification-preview">
    <div class="section process-log" v-if="processLog && processLog.length > 0">
      <h3>🔍 RAG 디버깅 로그</h3>
      <ul>
        <li v-for="(step, index) in processLog" :key="index">{{ step }}</li>
      </ul>
    </div>
    <div class="section message-section">
      <h3>📢 생성된 보고서</h3>
      <p v-if="message" class="message-text">{{ message }}</p>
      <p v-else class="empty-message">❌ 보고서가 생성되지 않았습니다.</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: String,
  processLog: Array,
});
</script>

<style scoped>
.notification-preview {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 12px;
  height: 100%;
}

.section h3 {
  font-size: 1.3rem;
  color: #4a4a4a;
  font-weight: 600;
  margin-bottom: 15px;
}

.process-log ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.process-log li {
  font-size: 1rem;
  color: #333;
  padding: 8px 12px;
  background: #ffffff;
  border-radius: 8px;
  margin-bottom: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.message-section {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.message-text {
  font-size: 1.1rem;
  color: #333;
  padding: 15px;
  background: #ffffff;
  border-radius: 8px;
  white-space: pre-wrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  flex-grow: 1;
}

.empty-message {
  font-size: 1rem;
  color: #ff6f61;
  text-align: center;
  padding: 15px;
}
</style>