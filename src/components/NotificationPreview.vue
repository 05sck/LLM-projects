<template>
    <div class="notification-preview">
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
    /* 스크롤 제거 */
    min-height: 100px;  /* 기본 최소 높이 */
    height: auto;  /* ✅ 내용이 추가될 때마다 높이 자동 조정 */
    padding: 10px;
    border-radius: 5px;
    background: #f9f9f9;
  }
  </style>
  