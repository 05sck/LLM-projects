import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Medication from "../pages/MedicationPage.vue";
import SchedulePage from "../pages/SchedulePage.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/schedule", component: SchedulePage },
  { path: "/medication", component: Medication } // 수정
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;