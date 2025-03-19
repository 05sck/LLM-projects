import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 🔥 Vue Router 추가
import { createPinia } from "pinia"; // 🔥 Pinia 상태 관리 추가

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount("#app");
