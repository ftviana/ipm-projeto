<script setup>
import { ref, computed } from 'vue'
import { store } from '../store.js'

const basePriceUSD = 124
const conversionRates = {
  USD: { symbol: '$', rate: 1.0 },
  EUR: { symbol: '€', rate: 0.94 },
  GBP: { symbol: '£', rate: 0.82 }
}

const displayedPrice = computed(() => {
  const info = conversionRates[store.state.currency]
  const price = (basePriceUSD * info.rate).toFixed(0)
  return info.symbol + price
})

const currentCurrencyInfo = computed(() => {
  return conversionRates[store.state.currency] || conversionRates.USD
})

const topNeighborhoods = ref([
  { id: 1, name: 'Chiado', occupancy: 80, price: 250 },
  { id: 2, name: 'Alfama', occupancy: 90, price: 160 },
  { id: 3, name: 'Belém', occupancy: 85, price: 180 },
  { id: 4, 'name': 'Bairro Alto', occupancy: 88, price: 190 },
  { id: 5, name: 'Graça', occupancy: 70, price: 140 },
  { id: 6, name: 'P. Nações', occupancy: 65, price: 150 },
])

const convertedTopNeighborhoods = computed(() => {
  const info = currentCurrencyInfo.value;
  return topNeighborhoods.value.map(item => {
    const convertedPrice = item.price * info.rate;
    return {
      ...item,
      price: convertedPrice,
      symbol: info.symbol
    };
  });
});

const insights = ref([
  { id: 1, text: '<strong>Chiado</strong> remains the priciest area, but neighborhoods like <strong>Alfama</strong> boast higher occupancy rates, highlighting a key price vs. demand dynamic.' },
  { id: 2, text: 'Seasonal trends are strong, with <strong>summer occupancy</strong> significantly outperforming winter, and an <strong>August peak</strong> in pricing.' },
  { id: 3, text: 'The market is dominated by <strong>single-property hosts</strong>, suggesting a fragmented landscape with fewer large-scale professional operations.' },
])

function getProgressStyle(occupancy) {
  return { '--progress-percent': `${occupancy}%` }
}
</script>

<template>
  <div class="explore-page">
    
    <div class="header">
      <div class="header-text">
        <h1>Explore Data</h1>
      </div>
      <button class="btn-report" @click="$router.push('/export')">Generate Report</button>
    </div>

    <div class="stats-grid">
      
      <div class="stat-card">
        <h3>Total Listings</h3>
        <div class="value-row">
          <p class="value">12,452</p>
          <div class="change positive">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            <span>5.2%</span>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>Avg. Price / Night</h3>
        <div class="value-row">
          <p class="value">{{ displayedPrice }}</p>
          <div class="change negative">
            <svg xmlns="http://www.w3.org/2TEst-ce" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>
            <span>1.8%</span>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>Avg. Review</h3>
        <div class="value-row">
          <p class="value">4.82</p>
          <div class="change positive">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            <span>0.5%</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <h3>Occupancy</h3>
        <div class="value-row">
          <p class="value">78%</p>
          <div class="change positive">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            <span>2.3%</span>
          </div>
        </div>
      </div>

    </div>

    <section class="card-container">
      <h3>Top 6 Neighborhoods — Price & Occupancy</h3>
      <div class="neighborhood-grid">
        <div v-for="item in convertedTopNeighborhoods" :key="item.id" class="neighborhood-item">
          <h4>{{ item.name }}</h4>
          <div class="progress-circle" :style="getProgressStyle(item.occupancy)">
            <span>{{ item.occupancy }}%</span>
          </div>
          <span class="neighborhood-price">{{ item.symbol }}{{ item.price.toFixed(0) }}</span>
        </div>
      </div>
    </section>

    <section class="card-container">
      <h3>Insights & Highlights</h3>
      <ul class="insights-list">
        <li v-for="item in insights" :key="item.id">
          <p v-html="item.text"></p>
        </li>
      </ul>
    </section>

  </div>
</template>

<style scoped>

.explore-page {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem 1rem 2rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.header h1 {
  font-weight: 800;
  font-size: 1.75rem;
  margin: 0;
  color: #111827;
}

.header .subtitle {
  font-size: 1rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.btn-report {
  background-color: #FF5A5F;
  color: #ffffff;
  border: none;
  padding: 0.6rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 9999px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  white-space: nowrap;
}

.btn-report:hover {
  background-color: #e05a5a;
}

.card-container,
.stat-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 4px 20px -5px rgba(150, 150, 150, 0.08);
  display: flex;
  flex-direction: column;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem; 
}

.stat-card {
  gap: 0.25rem; 
}

.stat-card h3 {
  font-size: 0.8rem; 
  font-weight: 500;
  color: #9ca3af;
  margin: 0 0 0.25rem 0;
}
        
.value-row {
  display: flex;
  align-items: baseline;
  gap: 0.35rem; 
}
        
.stat-card .value {
  font-size: 1.4rem; 
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1;
}
        
.stat-card .change {
  font-size: 0.75rem; 
  font-weight: 600;
}

.stat-card .change svg {
  width: 11px; 
  height: 11px;
  margin-right: 0.15rem; 
}

.stat-card .change.positive { color: #10B981; }
.stat-card .change.negative { color: #EF4444; }

.card-container h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
}

.neighborhood-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;
  text-align: center;
}

.neighborhood-item h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.5rem 0;
}

.progress-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: conic-gradient(#FF5A5F var(--progress-percent), #f3f4f6 0);
  position: relative;
  margin: 0 auto;
}

.progress-circle::before {
  content: '';
  position: absolute;
  width: 66px;
  height: 66px;
  background: #fff;
  border-radius: 50%;
}

.progress-circle span {
  position: relative;
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
}

.neighborhood-price {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #6b7280;
}

.insights-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.insights-list li {
  display: flex;
  align-items: flex-start;
}

.insights-list p {
  margin: 0;
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.6;
}

.insights-list p :deep(strong) {
  color: #111827;
  font-weight: 600;
}

</style>