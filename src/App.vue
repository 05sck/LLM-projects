<template>
  <DefaultLayout />
</template>

<script setup>
import DefaultLayout from "@/layouts/DefaultLayout.vue";
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}
#app {
  width: 100%;
  min-height: 100vh; /* ✅ 화면 크기만큼 최소 높이 유지 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* ✅ 위에서부터 확장 */
}
</style>
