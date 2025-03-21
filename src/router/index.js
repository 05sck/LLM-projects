import Home from "@/pages/Home.vue";
import MedicationPage from "@/pages/MedicationPage.vue";
import SchedulePage from "@/pages/SchedulePage.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/schedule', name: 'Schedule', component: SchedulePage },
  { path: '/medication', name: 'Medication', component: MedicationPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;