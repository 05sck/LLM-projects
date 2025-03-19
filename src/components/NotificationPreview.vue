<template>
    <div class="notification-preview">
      <h2>📢 알림 문자 미리보기</h2>
      <p v-if="message">{{ message }}</p>
      <p v-else>❌ 입력된 일정이 없습니다.</p>
    </div>
  </template>
  
  <script setup>
  defineProps({
    message: String
  });
  </script>
  
  <style scoped>
  .notification-preview {
    padding: 20px;
    border: 1px solid #ddd;
    background: #f8f9fa;
    text-align: left;
  }
  
  h2 {
    margin-bottom: 10px;
  }
  
  p {
    white-space: pre-line;
  }
  </style>
  