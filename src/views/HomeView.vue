<script setup>
import { computed } from 'vue'
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
</script>

<template>
  <div class="home-content">
    <section class="stats-boxes">
      <div class="box">
        <h3>Total Listings</h3>
        <div class="value-row">
          <p class="value">12,452</p>
          <div class="change positive">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            <span>5.2%</span>
          </div>
        </div>
      </div>
      <div class="box">
        <h3>Avg. Price</h3>
        <div class="value-row">
          <p class="value">{{ displayedPrice }}</p>
          <div class="change negative">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>
            <span>1.8%</span>
          </div>
        </div>
      </div>
      <div class="box">
        <h3>Avg. Review</h3>
        <div class="value-row">
          <p class="value">4.82</p>
          <div class="change positive">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            <span>0.5%</span>
          </div>
        </div>
      </div>
      <div class="box">
        <h3>Occupancy</h3>
        <div class="value-row">
          <p class="value">78%</p>
          <div class="change positive">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
            <span>2.3%</span>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-grid">
      <div class="cta-box cta-red">
        <h2>Explore Data</h2>
        <p>Dive into the city's data through our interactive maps and visualizations.</p>
        <RouterLink to ="/exploredata">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="M14.35 20.775L9 18.9l-4.65 1.8q-.25.1-.488.063t-.437-.163t-.312-.337T3 19.775V5.75q0-.325.188-.575T3.7 4.8l4.65-1.575q.15-.05.313-.075T9 3.125t.338.025t.312.075L15 5.1l4.65-1.8q.25-.1.488-.062t.437.162t.313.338t.112.487V18.25q0 .325-.187.575t-.513.375l-4.65 1.575q-.15.05-.312.075t-.338.025t-.337-.025t-.313-.075M14 18.55V6.85l-4-1.4v11.7zm2 0l3-1V5.7l-3 1.15zM5 18.3l3-1.15V5.45l-3 1zM16 6.85v11.7zm-8-1.4v11.7z"/></svg>
          <span>Explore Data</span>
        </RouterLink>
      </div>

      <div class="cta-box cta-blue">
        <h2>Anomalies</h2>
        <p>Get executive summaries on key anomalies and data trends.</p>
        <RouterLink to ="/anomalies">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="M10 21h4a2 2 0 0 1-2 2a2 2 0 0 1-2-2m11-2v1H3v-1l2-2v-6c0-3.1 2.03-5.83 5-6.71V4a2 2 0 0 1 2-2a2 2 0 0 1 2 2v.29c2.97.88 5 3.61 5 6.71v6zm-4-8a5 5 0 0 0-5-5a5 5 0 0 0-5 5v7h10zm2.75-7.81l-1.42 1.42A8.98 8.98 0 0 1 21 11h2c0-2.93-1.16-5.75-3.25-7.81M1 11h2c0-2.4.96-4.7 2.67-6.39L4.25 3.19A10.96 10.96 0 0 0 1 11"/></svg>
          <span>Anomalies</span>
        </RouterLink>
      </div>

      <div class="cta-box cta-yellow">
        <h2>Compare Cities</h2>
        <p>Benchmark cities against each other with our powerful comparison tools.</p>
        <RouterLink to ="/compare">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="M6 13H2c-.6 0-1 .4-1 1v8c0 .6.4 1 1 1h4c.6 0 1-.4 1-1v-8c0-.6-.4-1-1-1m16-4h-4c-.6 0-1 .4-1 1v12c0 .6.4 1 1 1h4c.6 0 1-.4 1-1V10c0-.6-.4-1-1-1m-8-8h-4c-.6 0-1 .4-1 1v20c0 .6.4 1 1 1h4c.6 0 1-.4 1-1V2c0-.6-.4-1-1-1"/></svg>
          <span>Compare</span>
        </RouterLink>
      </div>

      <div class="cta-box cta-purple">
        <h2>Export Data</h2>
        <p>Download comprehensive reports in various formats for your analysis.</p>
        <RouterLink to ="/export">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path fill="currentColor" d="m12 16l-5-5l1.4-1.45l2.6 2.6V4h2v8.15l2.6-2.6L17 11zm-6 4q-.825 0-1.412-.587T4 18v-3h2v3h12v-3h2v3q0 .825-.587 1.413T18 20z"/></svg>
          <span>Export Data</span>
        </RouterLink>
      </div>
    </section>

    <div class="separator">
      Or start by selecting a city
    </div>

    <div class="search-bar">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 21l-4.343-4.343m0 0A7.5 7.5 0 1 0 5.343 5.343a7.5 7.5 0 0 0 11.314 11.314"/></svg>
      <input type="text" placeholder="Search city (e.g. Lisbon, Porto, Paris...)" />
    </div>
  </div>
</template>

<style scoped>
.home-content {
  max-width: 785px;
  margin-left: auto;
  margin-right: auto;
  padding: 4rem 0;
}

.stats-boxes {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem; 
}

.box {
  flex: 1;
  background-color: white;
  padding: 1rem; 
  border-radius: 16px;
  box-shadow: 0 4px 20px -5px rgba(150, 150, 150, 0.08); 
}

.box h3 {
  font-size: 0.8rem; 
  font-weight: 500;
  color: dimgrey;
  margin: 0 0 0.25rem 0;
}

.value-row {
  display: flex;
  align-items: baseline;
  gap: 0.35rem; 
}

.box .value {
  font-size: 1.5rem; 
  font-weight: 700;
  color: black;
  margin: 0;
  line-height: 1;
}

.box .change {
  font-size: 0.75rem; 
  font-weight: 600;
}
.box .change svg {
  width: 11px; 
  height: 11px;
  margin-right: 0.15rem; 
}
.box .change.positive { color: #10B981; }
.box .change.negative { color: #FF5A5F; }

.cta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-auto-rows: 1fr;
  gap: 1rem;
}

.cta-box {
  padding: 1.25rem; 
  border-radius: 32px;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 1rem; 
}

/* COR ALTERADA */
.cta-red    { background-color: #FF5A5F; }
.cta-blue   { background-color: #32A9E1; }
.cta-yellow { background-color: #F5C544; }
.cta-purple { background-color: #7B61FF; }

.cta-box h2 {
  font-size: 1.15rem; 
  font-weight: 700;
  margin: 0;
}

.cta-box p {
  font-size: 0.8rem; 
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  line-height: 1.4; 
  flex-grow: 1;
}

.cta-box a {
  border-radius: 16px; 
  padding: 0.5rem 0.75rem; 
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem; 
  font-weight: 900;
  cursor: pointer;
  align-self: flex-start;
  transition: transform 0.2s ease;
  font-size: 0.8rem; 
  text-decoration: none;
  background-color: white;
}
.cta-box a:hover {
  transform: scale(1.05);
}
.cta-box a svg {
  width: 14px; 
  height: 14px;
  color: currentColor;
}

.cta-yellow a svg {
  transform: scaleX(-1);
}

/* COR ALTERADA */
.cta-red a {
  color: #FF5A5F;
}
.cta-blue a {
  color: #32A9E1;
}
.cta-yellow a {
  color: #F5C544;
}
.cta-purple a {
  color: #7B61FF;
}

.separator {
  display: flex;
  align-items: center;
  color: dimgrey;
  font-weight: 500;
  font-size: 0.9rem;
  margin: 2.5rem auto 1.5rem;
}

.separator::before,
.separator::after {
  content: '';
  flex-grow: 1;
  height: 1px;
  background-color: #ddd;
}

.separator::before {
  margin-right: 1rem;
}

.separator::after {
  margin-left: 1rem;
}

.search-bar {
  position: relative;
  margin-bottom: 2rem; 
}

.search-bar svg {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: dimgrey;
  width: 16px; 
  height: 16px;
}

/* ALTERAÇÃO AQUI: width para 100% */
.search-bar input {
  width: 100%;
  padding: 0.9rem 1.5rem 0.9rem 3rem; 
  border: none;
  border-radius: 9999px;
  background-color: white;
  font-size: 0.9rem;
  color: black;
}
.search-bar input::placeholder {
  color: dimgrey;
}
</style>