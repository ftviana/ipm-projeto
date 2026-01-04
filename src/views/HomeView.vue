<!-- 
  Vista Home - Página inicial da aplicação InsideView.
  
  Apresenta:
  - Estatísticas globais agregadas de todas as cidades (Total Listings, Preço Médio, Ocupação, Rating)
  - Grelha de CTAs para navegar para as funcionalidades principais
  
  Os dados são obtidos da API para todas as cidades e agregados para mostrar métricas globais.
-->
<template>
  <div class="home-content">
    <div v-if="isLoading" class="loading-state">
      <p>Loading platform insights...</p>
    </div>

    <section v-else class="stats-boxes">
      <div class="box">
        <h3>Total Listings</h3>
        <div class="value-row">
          <p class="value">{{ globalStats.count }}</p>
        </div>
      </div>

      <div class="box">
        <h3>Avg. Price/Night ({{ currencySymbol }})</h3>
        <div class="value-row">
          <p class="value">{{ currencySymbol }}{{ globalStats.price }}</p>
        </div>
      </div>

      <div class="box">
        <h3>Occupancy (%)</h3>
        <div class="value-row">
          <p class="value">{{ globalStats.occupancy }}%</p>
        </div>
      </div>

      <div class="box">
        <h3>Avg. Review (★)</h3>
        <div class="value-row">
          <div class="value">
            {{ globalStats.rating }}
            <span class="star-color">★</span>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-grid">
      <div class="cta-box cta-red">
        <div class="text-content">
          <h2>Explore Data</h2>
          <p>
            Dive into the city's data through our interactive maps and
            visualizations.
          </p>
        </div>
        <RouterLink to="/exploredata" class="cta-button">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7m0 9.5a2.5 2.5 0 0 1 0-5a2.5 2.5 0 0 1 0 5"
            />
          </svg>
          <span>Explore Data</span>
        </RouterLink>
      </div>

      <div class="cta-box cta-blue">
        <div class="text-content">
          <h2>Anomalies</h2>
          <p>Get executive summaries on key anomalies and data trends.</p>
        </div>
        <RouterLink to="/anomalies" class="cta-button">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2m6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1z"
            />
          </svg>
          <span>Anomalies</span>
        </RouterLink>
      </div>

      <div class="cta-box cta-yellow">
        <div class="text-content">
          <h2>Compare Cities</h2>
          <p>
            Benchmark cities against each other with our powerful comparison
            tools.
          </p>
        </div>
        <RouterLink to="/compare" class="cta-button">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2M9 17H7v-7h2zm4 0h-2v-3h2zm4 0h-2v-5h2z"
            />
          </svg>
          <span>Compare</span>
        </RouterLink>
      </div>

      <div class="cta-box cta-purple">
        <div class="text-content">
          <h2>Export Data</h2>
          <p>
            Download comprehensive reports in various formats for your analysis.
          </p>
        </div>
        <RouterLink to="/export" class="cta-button">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path fill="currentColor" d="M19 9h-4V3H9v6H5l7 7zM5 18v2h14v-2z" />
          </svg>
          <span>Export Data</span>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { store } from "../store.js";

const isLoading = ref(true);
const combinedData = ref([]);

// Taxas de conversão e símbolos para cada moeda suportada
const conversionRates = {
  USD: { symbol: "$", rate: 1.0 },
  EUR: { symbol: "€", rate: 0.94 },
  GBP: { symbol: "£", rate: 0.82 },
};

const currentCurrencyInfo = computed(
  () => conversionRates[store.state.currency] || conversionRates.USD
);
const currencySymbol = computed(() => currentCurrencyInfo.value.symbol);

/*
  Carrega os dados de todas as cidades (Porto, Lisboa, Barcelona) para o período selecionado.
  Os dados são combinados num único array para calcular estatísticas globais.
*/
const fetchAllCities = async () => {
  isLoading.value = true;
  const periodKey = store.state.period.replace("-", "_");
  try {
    const [resPorto, resLisbon, resBcn] = await Promise.all([
      fetch(`http://localhost:3000/porto_${periodKey}_listings`).then((r) =>
        r.ok ? r.json() : []
      ),
      fetch(`http://localhost:3000/lisbon_${periodKey}_listings`).then((r) =>
        r.ok ? r.json() : []
      ),
      fetch(`http://localhost:3000/barcelona_${periodKey}_listings`).then((r) =>
        r.ok ? r.json() : []
      ),
    ]);
    combinedData.value = [...resPorto, ...resLisbon, ...resBcn];
  } catch (e) {
    console.error("Error loading global data:", e);
  } finally {
    isLoading.value = false;
  }
};

/*
  Computed que calcula as estatísticas globais agregadas de todas as cidades:
  - count: número total de listings
  - price: preço médio por noite (convertido para a moeda selecionada)
  - occupancy: taxa de ocupação média (%)
  - rating: avaliação média (escala 0-5)
*/
const globalStats = computed(() => {
  const data = combinedData.value;
  if (!data.length) return { count: 0, price: 0, rating: 0, occupancy: 0 };

  let totalCount = 0,
    totalPrice = 0,
    totalRating = 0,
    validRatings = 0,
    totalOccupancy = 0;

  data.forEach((item) => {
    totalCount++;
    const p = parseFloat(String(item.price).replace(/[$,]/g, "")) || 0;
    totalPrice += p;
    if (item.review_scores_rating) {
      let r = parseFloat(item.review_scores_rating);
      if (r > 5) r /= 20;
      totalRating += r;
      validRatings++;
    }
    const avail = parseInt(item.availability_365) || 0;
    totalOccupancy += ((365 - avail) / 365) * 100;
  });

  const avgPrice =
    (totalCount > 0 ? totalPrice / totalCount : 0) *
    currentCurrencyInfo.value.rate;
  const avgRating = validRatings > 0 ? totalRating / validRatings : 0;
  const avgOcc = totalCount > 0 ? totalOccupancy / totalCount : 0;

  return {
    count: totalCount.toLocaleString(),
    price: Math.round(avgPrice),
    rating: avgRating.toFixed(2),
    occupancy: Math.round(avgOcc),
  };
});

onMounted(fetchAllCities);
</script>

<style scoped>
/* LAYOUT */
.home-content {
  width: 100%;
  max-width: 1000px;
  padding: 3rem 1rem;
  margin: 0 auto;
}

/* LOADING */
.loading-state {
  padding: 2rem;
  color: grey;
  text-align: center;
}

/* STATS BOXES */
.stats-boxes {
  display: flex;
  gap: 3rem;
  margin-bottom: 3rem;
}

.box {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1rem;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.02);
  border-radius: 16px;
  box-shadow: 0 4px 20px -5px rgba(150, 150, 150, 0.08);
}

.box h3 {
  margin: 0 0 0.25rem 0;
  font-size: 0.8rem;
  font-weight: 400;
  color: dimgrey;
}

.value-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.box .value {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  font-size: 1.6rem;
  font-weight: 700;
  color: black;
}

.star-color {
  color: gold;
}

/* CTA GRID */
.cta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-auto-rows: 1fr;
  gap: 1rem;
}

.cta-box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 230px;
  padding: 1.5rem;
  color: white;
  border-radius: 32px;
}

.cta-red {
  background-color: #ff5a5f;
}

.cta-blue {
  background-color: #32a9e1;
}

.cta-yellow {
  background-color: #f5c544;
}

.cta-purple {
  background-color: #7b61ff;
}

.text-content h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 700;
}

.text-content p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.9);
}

.cta-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  align-self: flex-start;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  font-weight: 700;
  background-color: white;
  border-radius: 24px;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.cta-button:hover {
  transform: scale(1.05);
}

.cta-button svg {
  width: 16px;
  height: 16px;
  color: currentColor;
}

.cta-red .cta-button {
  color: #ff5a5f;
}

.cta-blue .cta-button {
  color: #32a9e1;
}

.cta-yellow .cta-button {
  color: #f5c544;
}

.cta-yellow .cta-button svg {
  transform: scaleX(-1);
}

.cta-purple .cta-button {
  color: #7b61ff;
}
</style>
