/* 
  Ponto de entrada da aplicação InsideView.
  Inicializa a aplicação Vue, regista o router e monta no elemento #app.
*/
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.use(router);

app.mount("#app");
