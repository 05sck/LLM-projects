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
  min-height: 100vh; 
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
</style>
