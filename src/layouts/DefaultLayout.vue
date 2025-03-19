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
}

.content {
  margin-left: 220px; 
  padding: 20px;
  flex-grow: 1;
}
</style>
