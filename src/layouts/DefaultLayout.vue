<template>
  <div class="layout">
    <Sidebar /> <!-- ✅ 왼쪽 네비게이션 추가 -->
    <div class="content">
      <router-view />  <!-- ✅ 메인 컨텐츠 영역 -->
    </div>
  </div>
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue";
</script>

<style scoped>
.layout {
  display: flex;
}

.content {
  margin-left: 220px; /* 네비게이션 바 크기만큼 여백 */
  padding: 20px;
  flex-grow: 1;
}
</style>
