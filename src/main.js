import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";  // ✅ Pinia 추가

const app = createApp(App);

app.use(createPinia());  // ✅ Pinia 적용
app.use(router);
app.mount("#app");
