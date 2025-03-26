<template>
  <div class="notification-preview">
    <div v-if="processLog && processLog.length > 0" class="process-log">
      <h3>가져온 문서</h3>
      <ul>
        <li v-for="(step, index) in processLog" :key="index">{{ step }}</li>
      </ul>
    </div>
    <div class="message-section">
      <h3>결과 메시지</h3>
      <p v-if="message">{{ message }}</p>
      <p v-else>❌ 입력된 일정이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: String,
  processLog: Array  // process_log를 배열로 받음
});
</script>

<style scoped>
.notification-preview {
  min-height: 100px;  /* 기본 최소 높이 */
  height: auto;       /* 내용에 따라 높이 자동 조정 */
  padding: 15px;
  border-radius: 5px;
  background: #f9f9f9;
  text-align: left;
}

.process-log h3,
.message-section h3 {
  font-size: 1.2rem;
  color: #4a4a4a;
  margin-bottom: 10px;
}

.process-log ul {
  list-style-type: decimal;
  padding-left: 20px;
  margin: 0 0 20px 0;
}

.process-log li {
  font-size: 1rem;
  color: #333;
  margin: 5px 0;
  word-wrap: break-word;
}

.message-section p {
  font-size: 1rem;
  color: #333;
  margin: 0;
  white-space: pre-wrap;  /* 줄바꿈 유지 */
}
</style>