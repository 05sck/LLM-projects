import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue"; // 
import SchedulePage from "../pages/SchedulePage.vue"; 
import Medication from "../pages/MedicationPage.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/schedule", component: SchedulePage }, 
  { path: "/medication", component: MedicationPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
