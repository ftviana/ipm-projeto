/* 
  Configuração do Vue Router para a aplicação InsideView.
  
  Define as rotas da aplicação, todas aninhadas dentro do DefaultLayout:
  - / (Home): página inicial com estatísticas globais
  - /exploredata: exploração de dados por cidade
  - /compare: comparação entre cidades
  - /anomalies: deteção de anomalias nos dados
  - /export: exportação de relatórios
  - /faq: perguntas frequentes
*/
import { createRouter, createWebHistory } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import ExploreDataView from "../views/ExploreDataView.vue";
import CompareView from "../views/CompareView.vue";
import AnomaliesView from "../views/AnomaliesView.vue";
import ExportView from "../views/ExportView.vue";
import FAQView from "../views/FAQView.vue";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      { path: "", name: "", component: HomeView },
      { path: "exploredata", name: "exploredata", component: ExploreDataView },
      { path: "compare", name: "compare", component: CompareView },
      { path: "anomalies", name: "anomalies", component: AnomaliesView },
      { path: "export", name: "export", component: ExportView },
      { path: "faq", name: "faq", component: FAQView },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
