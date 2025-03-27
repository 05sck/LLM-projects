<template>
  <div class="layout">
    <Sidebar />
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue";
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh; /* 전체 화면 높이 확보 */
  background: #ffffff; /* 기본 배경을 흰색으로 설정 */
}

.content {
  margin-left: 140px; /* Sidebar 너비(70px) + padding(25px * 2) 고려 */
  padding: 0; /* MedicationPage.vue에서 패딩을 제어하도록 */
  flex-grow: 1;
  background: #ffffff; /* 콘텐츠 영역도 흰색으로 */
}
</style>