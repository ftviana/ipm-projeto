import { createRouter, createWebHistory } from 'vue-router';

import GamePage from './pages/GamePage.vue';
import StatisticsPage from './pages/StatisticsPage.vue';
import SimulationPage from './pages/SimulationPage.vue';
import NotFoundPage from './pages/NotFoundPage.vue';
import GameResultPage from './pages/GameResultPage.vue';

// TODO: criar a função validateSimulation(to, from)
// A função deve:
//  1. Obter a store de simulação
//  2. Verificar se existe simulação (store.containsSimulation)
//  3. Se existir → return true
//  4. Caso contrário → mostrar toast informando que não há simulação
//  5. Redirecionar para "/game"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/game'
    },
    {
      path: '/game',
      component: GamePage
    },
    {
      path: '/game/:id',
      component: GameResultPage,
      props: true
    },
    {
      path: '/statistics',
      component: StatisticsPage
    },
    {
      path: '/simulation',
      component: SimulationPage
    },
    {
      path: '/:notFound(.*)',
      component: NotFoundPage
    }
  ]
});

export default router;