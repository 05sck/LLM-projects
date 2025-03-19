import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue"; // ✅ 절대 경로 대신 상대 경로 사용
import Schedule from "../pages/Schedule.vue";
import Medication from "../pages/Medication.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/schedule", component: Schedule },
  { path: "/medication", component: Medication }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
