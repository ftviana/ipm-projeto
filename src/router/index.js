import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import ExploreDataView from '../views/ExploreDataView.vue'
import CompareView from '../views/CompareView.vue'
import AnomaliesView from '../views/AnomaliesView.vue'
import ExportView from '../views/ExportView.vue'
import FAQView from '../views/FAQView.vue'
import HomeView from '../views/HomeView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: '',
        component: HomeView
      },
      {
        path: 'exploredata', // Renders at '/exploredata'
        name: 'exploredata',
        component: ExploreDataView
      },
      {
        path: 'compare', // Renders at '/compare'
        name: 'compare',
        component: CompareView
      },
      {
        path: 'anomalies', // Renders at '/anomalies'
        name: 'anomalies',
        component: AnomaliesView
      },
      {
        path: 'export', // Renders at '/export'
        name: 'export',
        component: ExportView
      },
      {
        path: 'faq', // Renders at '/faq'
        name: 'faq',
        component: FAQView
      },
      {
        path: 'settings', // Will be /settings
        name: 'settings',
        component: SettingsView
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router