import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue"; // ✅ 그대로 유지
import SchedulePage from "../views/SchedulePage.vue"; // ✅ 변경된 파일 경로
import Medication from "../pages/Medication.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/schedule", component: SchedulePage }, // ✅ 변경
  { path: "/medication", component: Medication }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
