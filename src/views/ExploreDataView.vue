<template>
  <div class="explore-container">
    <div class="header-section">
      <div class="header-left">
        <h1>Explore Data</h1>
        
        <div class="filter-row">
          <button class="btn-outline-primary" @click="toggleSidebar">
            {{ isSidebarOpen ? 'Close Filters' : 'Open Filters' }}
          </button>

          <div class="filter-tags" v-if="activeTags.length > 0">
            <div v-for="(tag, index) in activeTags" :key="index" class="filter-tag">
              <span>{{ tag.label }}: {{ tag.value }}</span>
              <button @click="removeFilter(tag.key)" class="close-tag">×</button>
            </div>
            <button @click="resetFilters" class="clear-all-text">Clear all</button>
          </div>
        </div>
      </div>
      
      <div class="header-actions">
        <button class="btn-primary">Generate Report</button>
      </div>
    </div>

    <div class="kpi-grid">
      <div v-if="isLoading" class="loading-card full-width">
        <p>Loading data from local CSV...</p>
      </div>

      <div v-else-if="errorMessage" class="error-card full-width">
        <p>⚠️ {{ errorMessage }}</p>
        <small>Check console for details.</small>
      </div>

      <template v-else>
        <div class="card kpi-card">
          <h3>Active Listings</h3>
          <div class="kpi-value">{{ formattedMetrics.count }}</div>
          <div class="kpi-subtext" style="color: #10B981">↑ +5.2% vs last year</div>
        </div>
        <div class="card kpi-card">
          <h3>Avg. Price / Night ({{ currencySymbol }})</h3>
          <div class="kpi-value">{{ currencySymbol }}{{ formattedMetrics.price }}</div>
           <div class="kpi-subtext" style="color: #FF5A5F">↓ -2.1% vs last year</div>
        </div>
        <div class="card kpi-card">
          <h3>Occupancy Rate (%)</h3>
          <div class="kpi-value">{{ formattedMetrics.occupancy }}%</div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: formattedMetrics.occupancy + '%' }"></div>
          </div>
        </div>
        <div class="card kpi-card">
          <h3>Average Rating (★)</h3>
          <div class="kpi-value">
            {{ formattedMetrics.rating }} 
            <span class="star-color">★</span>
          </div>
          <div class="kpi-subtext">Based on filtered reviews</div>
        </div>
      </template>
    </div>

    <div class="card heatmap-section">
      <div class="card-header">
        <h3>Geospatial Heatmap</h3>
        <div class="toggle-switch">
          <button :class="{ active: heatmapMode === 'Price' }" @click="heatmapMode = 'Price'">Price</button>
          <button :class="{ active: heatmapMode === 'Occupancy' }" @click="heatmapMode = 'Occupancy'">Occupancy</button>
        </div>
      </div>
      <div class="map-placeholder">
        <p style="color: dimgrey;">[ Map Visualization Placeholder ]</p>
      </div>
      <div class="map-footer">
        <span class="lightbulb-icon">💡</span>
        <p>The heatmap reveals the highest price intensity is concentrated in the historic city center.</p>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h3>Avg. Monthly Price — Last Season</h3>
        <div class="chart-placeholder"></div>
      </div>
      <div class="card chart-card">
        <h3>Monthly Occupancy Trend</h3>
        <div class="chart-placeholder"></div>
      </div>
    </div>

    <div class="card full-width-card">
      <h3>Top Neighborhoods — Price & Occupancy</h3>
      <div class="list-placeholder"></div>
    </div>

    <div class="sidebar" :class="{ open: isSidebarOpen }">
      <div class="sidebar-header">
        <div class="sidebar-title">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M22 3H2l8 9.46V19l4 2v-8.54z"/></svg>
          <h2>Filters</h2>
        </div>
      </div>

      <div class="sidebar-content">
        
        <div class="filter-group">
          <label>City</label>
          <div class="input-wrapper">
            <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path stroke="currentColor" stroke-width="2" d="m21 21l-4.35-4.35"/></svg>
            <input type="text" v-model="stagingFilters.city" placeholder="Lisbon" />
          </div>
        </div>

        <div class="filter-group">
          <label>Neighborhood</label>
          <div class="select-wrapper">
             <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 7.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            <select v-model="stagingFilters.neighborhood">
              <option value="">All Neighborhoods</option>
              <option v-for="neigh in uniqueNeighborhoods" :key="neigh" :value="neigh">{{ neigh }}</option>
            </select>
          </div>
        </div>

        <div class="filter-group">
          <label>Property Type</label>
          <div class="select-wrapper">
            <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9l9-7l9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            <select v-model="stagingFilters.propertyType">
              <option value="">All Types</option>
              <option value="Entire home/apt">Entire home/apt</option>
              <option value="Private room">Private room</option>
              <option value="Shared room">Shared room</option>
            </select>
          </div>
        </div>

        <div class="filter-group">
          <div class="range-header">
            <label>Price Range (€)</label>
          </div>
          <input type="range" v-model.number="stagingFilters.priceMax" min="0" max="1000" step="10" class="styled-slider">
          <div class="range-labels">
            <span>€0</span>
            <span>€{{ stagingFilters.priceMax }}+</span>
          </div>
        </div>

        <div class="filter-group">
          <div class="range-header">
            <label>Rating (★)</label>
          </div>
          <input type="range" v-model.number="stagingFilters.minRating" min="0" max="5" step="0.1" class="styled-slider">
          <div class="range-labels">
            <span>{{ stagingFilters.minRating }} ★</span>
            <span>5.0 ★</span>
          </div>
        </div>

        <div class="filter-group">
          <label>Date Range</label>
          <div class="date-buttons">
             <button class="date-btn">Last 7 days</button>
             <button class="date-btn">Last 3 months</button>
             <button class="date-btn active">Custom</button>
          </div>
          <div class="date-inputs">
            <div class="input-wrapper date">
               <input type="text" placeholder="2023-10-01">
            </div>
            <div class="input-wrapper date">
               <input type="text" placeholder="2023-12-31">
            </div>
          </div>
        </div>

      </div>

      <div class="sidebar-footer">
        <button class="btn-apply" @click="applyFilters">Apply Filters</button>
        <button class="btn-clear" @click="resetFilters">Clear All</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import { store } from '../store.js';
import Papa from 'papaparse';

const heatmapMode = ref('Price');
const rawListings = ref([]);
const isLoading = ref(true);
const errorMessage = ref(null);
const isSidebarOpen = ref(false);

const stagingFilters = reactive({
  city: '', neighborhood: '', propertyType: '', priceMax: 1000, minRating: 0
});

const appliedFilters = reactive({
  city: '', neighborhood: '', propertyType: '', priceMax: 1000, minRating: 0
});

const conversionRates = {
  USD: { rate: 1.0, symbol: '$' },
  EUR: { rate: 0.94, symbol: '€' },
  GBP: { rate: 0.82, symbol: '£' }
};

const toggleSidebar = () => {
  if (!isSidebarOpen.value) { Object.assign(stagingFilters, appliedFilters); }
  isSidebarOpen.value = !isSidebarOpen.value;
};

const applyFilters = () => {
  Object.assign(appliedFilters, stagingFilters);
  isSidebarOpen.value = false;
};

const resetFilters = () => {
  const defaults = { city: '', neighborhood: '', propertyType: '', priceMax: 1000, minRating: 0 };
  Object.assign(stagingFilters, defaults);
  Object.assign(appliedFilters, defaults);
};

const removeFilter = (key) => {
  if (key === 'priceMax') appliedFilters.priceMax = 1000;
  else if (key === 'minRating') appliedFilters.minRating = 0;
  else appliedFilters[key] = '';
  Object.assign(stagingFilters, appliedFilters);
};

const loadData = () => {
  isLoading.value = true;
  Papa.parse('/data/listings.csv', {
    download: true, header: true, skipEmptyLines: true, dynamicTyping: true,
    complete: (results) => {
      if (!results.data?.length) { errorMessage.value = "File empty."; isLoading.value = false; return; }
      if (!results.data[0].hasOwnProperty('price')) { errorMessage.value = "Missing 'price' column."; isLoading.value = false; return; }
      rawListings.value = results.data; isLoading.value = false;
    },
    error: (err) => { errorMessage.value = "Failed to load CSV."; isLoading.value = false; }
  });
};

onMounted(() => loadData());

const currentCurrencyInfo = computed(() => conversionRates[store.state.currency] || conversionRates.USD);
const currencySymbol = computed(() => currentCurrencyInfo.value.symbol);

const cleanPrice = (val) => {
  if (typeof val === 'number') return val;
  if (!val) return 0;
  return parseFloat(String(val).replace(/[$,]/g, '')) || 0;
};

const uniqueNeighborhoods = computed(() => {
  const hoods = new Set();
  rawListings.value.forEach(item => {
    const n = item.neighbourhood_cleansed || item.neighbourhood; 
    if (n) hoods.add(n);
  });
  return Array.from(hoods).sort();
});

const filteredListings = computed(() => {
  return rawListings.value.filter(item => {
    const price = cleanPrice(item.price);
    if (price > appliedFilters.priceMax) return false;
    const n = item.neighbourhood_cleansed || item.neighbourhood;
    if (appliedFilters.neighborhood && n !== appliedFilters.neighborhood) return false;
    if (appliedFilters.propertyType && item.room_type !== appliedFilters.propertyType) return false;
    let rating = parseFloat(item.review_scores_rating || 0);
    let normalizedRating = rating;
    if (rating > 5) normalizedRating = rating / 20; 
    if (normalizedRating < appliedFilters.minRating) return false;
    return true;
  });
});

const activeTags = computed(() => {
  const tags = [];
  if (appliedFilters.neighborhood) tags.push({ key: 'neighborhood', label: 'Hood', value: appliedFilters.neighborhood });
  if (appliedFilters.propertyType) tags.push({ key: 'propertyType', label: 'Type', value: appliedFilters.propertyType });
  if (appliedFilters.priceMax < 1000) tags.push({ key: 'priceMax', label: 'Price', value: `< €${appliedFilters.priceMax}` });
  if (appliedFilters.minRating > 0) tags.push({ key: 'minRating', label: 'Rating', value: `${appliedFilters.minRating}+ ★` });
  return tags;
});

const formattedMetrics = computed(() => {
  const data = filteredListings.value;
  if (data.length === 0) return { count: 0, price: 0, occupancy: 0, rating: 0 };
  const count = data.length;
  let totalPrice = 0; let validPriceCount = 0; let totalAvailability = 0; let totalRating = 0; let validRatingCount = 0;
  for (let i = 0; i < count; i++) {
    const item = data[i];
    const p = cleanPrice(item.price);
    if (p > 0) { totalPrice += p; validPriceCount++; }
    const avail = item.availability_365 !== undefined ? item.availability_365 : 0;
    totalAvailability += avail;
    if (item.review_scores_rating) { totalRating += parseFloat(item.review_scores_rating); validRatingCount++; }
  }
  const avgBasePrice = validPriceCount > 0 ? (totalPrice / validPriceCount) : 0;
  const convertedPrice = avgBasePrice * currentCurrencyInfo.value.rate;
  const avgAvailability = totalAvailability / count;
  const occupancyRate = ((365 - avgAvailability) / 365) * 100;
  let finalRating = validRatingCount > 0 ? (totalRating / validRatingCount) : 0;
  if (finalRating > 5) finalRating = finalRating / 20; 
  return { count: count.toLocaleString(), price: Math.round(convertedPrice), occupancy: Math.round(occupancyRate), rating: finalRating.toFixed(2) };
});
</script>

<style scoped>
.explore-container {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 820px;
  margin: 0 auto;
  color: black;
}

/* --- HEADER --- */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; 
  margin-bottom: 2rem; 
}

.header-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  flex: 1;
}

.header-left h1 {
  font-weight: 800; font-size: 2rem; margin: 0 0 0.5rem 0; color: black;
}

.header-actions {
  margin-top: 5px; 
}

.filter-row { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; width: 100%; }
.filter-tags { display: contents; }
@supports not (display: contents) { .filter-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; } }

/* Cores alteradas aqui */
.filter-tag { display: flex; align-items: center; background-color: white; color: #FF5A5F; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; gap: 8px; white-space: nowrap; }
.close-tag { background: none; border: none; color: #FF5A5F; font-size: 1.1rem; cursor: pointer; padding: 0; }
.clear-all-text { background: none; border: none; color: dimgrey; text-decoration: underline; cursor: pointer; font-size: 0.85rem; white-space: nowrap; }

/* Cores alteradas aqui */
.btn-primary { background-color: #FF5A5F; color: white; border: none; padding: 10px 24px; border-radius: 30px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 10px rgba(255, 90, 95, 0.2); margin: 6px; white-space: nowrap; }
.btn-primary:hover { background-color: #e0484d; }
.btn-outline-primary { border: 2px solid #FF5A5F; color: #FF5A5F; background: transparent; padding: 8px 16px; border-radius: 20px; font-weight: 600; cursor: pointer; transition: background-color 0.2s; white-space: nowrap; }
.btn-outline-primary:hover { background-color: rgba(255, 90, 95, 0.05); }

/* --- SIDEBAR --- */
.sidebar {
  position: fixed; 
  top: 114px; 
  left: -350px; 
  width: 280px; 
  height: calc(100vh - 106px); 
  
  background-color: transparent; 
  
  z-index: 900;
  box-shadow: none;
  border: none;
  
  overflow-y: auto; 
  transition: left 0.3s ease-in-out;
  display: flex; flex-direction: column;
}

.sidebar.open { left: 0; box-shadow: none; }

.sidebar-header { padding: 0 1.5rem 1.5rem 1.5rem; }
.sidebar-title { display: flex; align-items: center; gap: 10px; color: black; }
.sidebar-title h2 { margin: 0; font-size: 1.5rem; font-weight: 700; }

.sidebar-content {
  padding: 0rem 1.5rem;
  display: flex; flex-direction: column; gap: 1.5rem;
}

.filter-group label { display: block; font-weight: 700; margin-bottom: 0.5rem; color: black; font-size: 0.95rem;}
.input-wrapper, .select-wrapper { position: relative; display: flex; align-items: center; }
.input-icon { position: absolute; left: 12px; color: dimgrey; z-index: 1;}
.sidebar input[type="text"], .sidebar select { width: 100%; padding: 10px 12px 10px 36px; border: 1px solid lightgrey; border-radius: 12px; font-size: 0.9rem; color: black; outline: none; appearance: none; background: white; }
.sidebar select { cursor: pointer; background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22dimgrey%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E"); background-repeat: no-repeat; background-position: right 1rem top 50%; background-size: 0.65rem auto; padding-right: 2rem; }
.styled-slider { width: 100%; height: 6px; background: lightgrey; border-radius: 5px; outline: none; appearance: none; -webkit-appearance: none; }
/* Cor alterada aqui */
.styled-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; border-radius: 50%; background: #FF5A5F; cursor: pointer; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.range-labels { display: flex; justify-content: space-between; font-size: 0.85rem; color: dimgrey; margin-top: 5px;}
.date-buttons { display: flex; gap: 8px; margin-bottom: 10px; }
.date-btn { flex: 1; padding: 8px; font-size: 0.8rem; border: 1px solid lightgrey; border-radius: 8px; background: white; cursor: pointer; color: dimgrey; }
/* Cor alterada aqui */
.date-btn.active { background: #FF5A5F; color: white; border-color: #FF5A5F; }
.date-inputs { display: flex; gap: 10px; }
.date-inputs .input-wrapper { flex: 1; }
.date-inputs input { padding-left: 12px; }

.sidebar-footer { padding: 1.5rem; border-top: 1px solid transparent; display: flex; flex-direction: column; gap: 10px; margin-top: auto; }
/* Cor alterada aqui */
.btn-apply { width: 100%; background: #FF5A5F; color: white; padding: 12px; border-radius: 12px; border: none; font-weight: 600; cursor: pointer; }
.btn-clear { width: 100%; background: white; color: black; padding: 12px; border-radius: 12px; border: 1px solid lightgrey; font-weight: 600; cursor: pointer; }

.card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.02); }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
.kpi-card h3 { font-size: 0.9rem; color: dimgrey; margin-bottom: 0.5rem; font-weight: 500; }
.kpi-value { font-size: 1.8rem; font-weight: 700; margin-bottom: 0.2rem; color: black; }
.kpi-subtext { font-size: 0.8rem; font-weight: 500; }
.progress-bar { width: 100%; height: 8px; background: lightgrey; border-radius: 4px; margin-top: 10px; overflow: hidden; }
/* Cor alterada aqui */
.progress-fill { height: 100%; background: #FF5A5F; border-radius: 4px; }
.star-color { color: gold; }
.heatmap-section { margin-bottom: 2rem; min-height: 400px; display: flex; flex-direction: column; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.toggle-switch { background: lightgrey; border-radius: 20px; padding: 4px; display: flex; }
.toggle-switch button { border: none; background: transparent; padding: 6px 16px; border-radius: 16px; cursor: pointer; font-size: 0.85rem; font-weight: 500; color: black; }
/* Cor alterada aqui */
.toggle-switch button.active { background: #FF5A5F; color: white; box-shadow: 0 2px 4px black; }
.map-placeholder { background-color: lightgrey; flex: 1; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem; }
.map-footer { color: dimgrey; display: flex; gap: 0.5rem; align-items: center; font-size: 0.85rem; }
.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem; }
.chart-card { min-height: 300px; }
.full-width-card { margin-bottom: 2rem; min-height: 250px; }
.loading-card, .error-card { background: white; padding: 2rem; border-radius: 16px; text-align: center; grid-column: 1 / -1; }
/* Cor alterada aqui */
.error-card { border-left: 4px solid #FF5A5F; color: #FF5A5F; }
</style>