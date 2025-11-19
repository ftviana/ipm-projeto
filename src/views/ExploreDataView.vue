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
            <div class="filter-tag city-tag">
              <span>City: {{ formatCityName(appliedFilters.city) }}</span>
            </div>

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
        <p>Loading data for {{ formatCityName(appliedFilters.city) }}...</p>
      </div>

      <div v-else-if="errorMessage" class="error-card full-width">
        <p>⚠️ {{ errorMessage }}</p>
      </div>

      <template v-else>
        <div class="card kpi-card">
          <h3>Active Listings</h3>
          <div class="kpi-value">{{ formattedMetrics.count }}</div>
          <div class="kpi-subtext" :class="getTrendClass(formattedMetrics.trends.count)">
            <span v-if="formattedMetrics.trends.count > 0">↑</span>
            <span v-else>↓</span>
            {{ Math.abs(formattedMetrics.trends.count) }}% vs last year
          </div>
        </div>

        <div class="card kpi-card">
          <h3>Avg. Price/Night ({{ currencySymbol }})</h3>
          <div class="kpi-value">{{ currencySymbol }}{{ formattedMetrics.price }}</div>
           <div class="kpi-subtext" :class="getTrendClass(formattedMetrics.trends.price)">
            <span v-if="formattedMetrics.trends.price > 0">↑</span>
            <span v-else>↓</span>
            {{ Math.abs(formattedMetrics.trends.price) }}% vs last year
           </div>
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
          <div class="kpi-subtext">Based on {{ formattedMetrics.reviewsCount }} reviews</div>
        </div>
      </template>
    </div>

    <div class="card heatmap-section">
      <div class="card-header">
        <h3>Geospatial Heatmap — {{ formatCityName(appliedFilters.city) }}</h3>
        <div class="toggle-switch">
          <button :class="{ active: heatmapMode === 'Price' }" @click="heatmapMode = 'Price'">Price</button>
          <button :class="{ active: heatmapMode === 'Occupancy' }" @click="heatmapMode = 'Occupancy'">Occupancy</button>
        </div>
      </div>
      <div class="map-placeholder">
        <p style="color: grey;">[ Map Visualization Placeholder ]</p>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h3>Avg. Monthly Price — Last Season</h3>
        <div class="chart-placeholder">
          <svg viewBox="0 0 100 40" class="simple-chart">
            <path d="M0 35 L20 32 L40 28 L60 15 L80 25" fill="none" stroke="#FF5A5F" stroke-width="1" />
          </svg>
          <div class="chart-labels">
             <span>May</span><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span>
          </div>
        </div>
      </div>

      <div class="card chart-card">
        <h3>Monthly Occupancy Trend</h3>
        <div class="chart-placeholder">
          <svg viewBox="0 0 100 40" class="simple-chart">
            <path d="M0 35 Q50 5 100 35" fill="none" stroke="black" stroke-width="1" />
          </svg>
           <div class="chart-labels">
             <span>Jan</span><span>Mar</span><span>May</span><span>Jul</span><span>Sep</span><span>Dec</span>
          </div>
        </div>
      </div>
    </div>

    <div class="card full-width-card">
      <h3>Top 6 Neighborhoods — Price & Occupancy</h3>
      
      <div v-if="topNeighborhoods.length > 0" class="circles-container">
        <div v-for="(item, index) in topNeighborhoods" :key="index" class="circle-item">
          <h4>{{ item.name }}</h4>
          <div class="circle">
            <span class="circle-value">{{ item.occupancy }}%</span>
          </div>
          <span class="circle-price">{{ currencySymbol }}{{ item.price }}</span>
        </div>
      </div>
      <div v-else class="loading-text">
        Calculating neighborhood data...
      </div>
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
          <label>Select City</label>
          <div class="select-wrapper">
            <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21h18M5 21V7l8-4l8 4v14M8 9v2m0 4v2m8-8v2m0 4v2m-4-8v2m0 4v2"/></svg>
            <select v-model="stagingFilters.city">
              <option value="porto">Porto</option>
              <option value="lisbon">Lisbon</option>
              <option value="barcelona">Barcelona</option>
            </select>
          </div>
        </div>

        <div class="filter-group" :class="{ disabled: stagingFilters.city !== appliedFilters.city }">
          <label>Neighborhood</label>
          <div class="select-wrapper">
             <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 7.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            <select v-model="stagingFilters.neighborhood" :disabled="stagingFilters.city !== appliedFilters.city">
              <option value="">All Neighborhoods</option>
              <option v-for="neigh in uniqueNeighborhoods" :key="neigh" :value="neigh">{{ neigh }}</option>
            </select>
          </div>
          <small v-if="stagingFilters.city !== appliedFilters.city" style="color: #FF5A5F; font-size: 0.75rem;">
            Apply city change to enable neighborhoods.
          </small>
        </div>

        <div class="filter-group" :class="{ disabled: stagingFilters.city !== appliedFilters.city }">
          <label>Property Type</label>
          <div class="select-wrapper">
            <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9l9-7l9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            <select v-model="stagingFilters.propertyType" :disabled="stagingFilters.city !== appliedFilters.city">
              <option value="">All Types</option>
              <option value="Entire home/apt">Entire home/apt</option>
              <option value="Private room">Private room</option>
              <option value="Shared room">Shared room</option>
              <option value="Hotel room">Hotel room</option>
            </select>
          </div>
        </div>

        <div class="filter-group">
          <div class="range-header">
            <label>Price Range (€)</label>
          </div>
          <div class="multi-range-slider">
            <div class="slider-track">
              <div class="range-color" :style="sliderTrackStyle"></div>
            </div>
            <input type="range" v-model.number="stagingFilters.priceMin" min="0" max="1000" step="10" @input="validatePriceMin">
            <input type="range" v-model.number="stagingFilters.priceMax" min="0" max="1000" step="10" @input="validatePriceMax">
          </div>
          <div class="range-labels">
            <span>€{{ stagingFilters.priceMin }}</span>
            <span>€{{ stagingFilters.priceMax }}<span v-if="stagingFilters.priceMax >= 1000">+</span></span>
          </div>
        </div>

        <div class="filter-group">
          <div class="range-header">
            <label>Rating (★)</label>
          </div>
          <input type="range" v-model.number="stagingFilters.minRating" min="1" max="5" step="1" class="styled-slider">
          <div class="range-labels">
            <span>{{ stagingFilters.minRating }}<span v-if="stagingFilters.minRating < 5">+</span> ★</span>
            <span>5 ★</span>
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

// --- ESTADO ---
const heatmapMode = ref('Price');
const rawListings = ref([]); 
const historyListings = ref([]); 
const isLoading = ref(true);
const errorMessage = ref(null);
const isSidebarOpen = ref(false);

// 1. Filtros Iniciais (Default: Porto) - CRÍTICO PARA O ARRANQUE
const stagingFilters = reactive({
  city: 'porto', neighborhood: '', propertyType: '', priceMin: 0, priceMax: 1000, minRating: 1
});
const appliedFilters = reactive({
  city: 'porto', neighborhood: '', propertyType: '', priceMin: 0, priceMax: 1000, minRating: 1
});

const conversionRates = {
  USD: { rate: 1.0, symbol: '$' },
  EUR: { rate: 0.94, symbol: '€' },
  GBP: { rate: 0.82, symbol: '£' }
};

// --- ACTIONS ---
const validatePriceMin = () => {
  if (stagingFilters.priceMin > stagingFilters.priceMax) stagingFilters.priceMin = stagingFilters.priceMax;
};
const validatePriceMax = () => {
  if (stagingFilters.priceMax < stagingFilters.priceMin) stagingFilters.priceMax = stagingFilters.priceMin;
};
const sliderTrackStyle = computed(() => {
  const min = (stagingFilters.priceMin / 1000) * 100;
  const max = (stagingFilters.priceMax / 1000) * 100;
  return { left: `${min}%`, width: `${max - min}%` };
});

const toggleSidebar = () => {
  if (!isSidebarOpen.value) Object.assign(stagingFilters, appliedFilters);
  isSidebarOpen.value = !isSidebarOpen.value;
};

const applyFilters = () => {
  const cityChanged = stagingFilters.city !== appliedFilters.city;
  Object.assign(appliedFilters, stagingFilters);
  if (cityChanged) {
    stagingFilters.neighborhood = '';
    appliedFilters.neighborhood = '';
    loadData();
  }
  isSidebarOpen.value = false;
};

const resetFilters = () => {
  // Reseta para os defaults da cidade atual (não muda a cidade)
  const currentCity = appliedFilters.city;
  const defaults = { city: currentCity, neighborhood: '', propertyType: '', priceMin: 0, priceMax: 1000, minRating: 1 };
  Object.assign(stagingFilters, defaults);
  Object.assign(appliedFilters, defaults);
};

const removeFilter = (key) => {
  if (key === 'priceRange') { appliedFilters.priceMin = 0; appliedFilters.priceMax = 1000; }
  else if (key === 'minRating') appliedFilters.minRating = 1;
  else appliedFilters[key] = '';
  Object.assign(stagingFilters, appliedFilters);
};

// --- DATA LOADING ---
const loadData = () => {
  // Garante que há uma cidade antes de tentar carregar
  const cityFolder = appliedFilters.city || 'porto';
  
  isLoading.value = true;
  errorMessage.value = null;
  
  rawListings.value = [];
  historyListings.value = [];

  const currentFile = `/data/${cityFolder}/listings.csv`; 
  const historyFile = `/data/${cityFolder}/history/12_months.csv`; 

  const parseFile = (url) => {
    return new Promise((resolve, reject) => {
      Papa.parse(url, {
        download: true, header: true, skipEmptyLines: true, dynamicTyping: true,
        complete: (results) => resolve(results.data),
        error: (err) => reject(err)
      });
    });
  };

  console.log(`Loading data for: ${cityFolder}`);

  parseFile(currentFile)
    .then(currentData => {
      if (!currentData || !currentData.length) throw new Error("File empty or not found.");
      rawListings.value = currentData;
      
      parseFile(historyFile)
        .then(historyData => { historyListings.value = historyData; })
        .catch(() => console.warn(`History file missing for ${cityFolder}`))
        .finally(() => { isLoading.value = false; });
    })
    .catch((err) => {
      console.error(err);
      errorMessage.value = `Failed to load data for ${formatCityName(cityFolder)}. Check public/data folders.`;
      isLoading.value = false;
    });
};

onMounted(() => loadData());

// --- HELPERS ---
const formatCityName = (val) => val ? val.charAt(0).toUpperCase() + val.slice(1) : '';
const currentCurrencyInfo = computed(() => conversionRates[store.state.currency] || conversionRates.USD);
const currencySymbol = computed(() => currentCurrencyInfo.value.symbol);

const cleanPrice = (val) => {
  if (typeof val === 'number') return val;
  if (!val) return 0;
  return parseFloat(String(val).replace(/[$,]/g, '')) || 0;
};

const getTrendClass = (val) => {
  if (!isFinite(val)) return 'trend-positive';
  return val >= 0 ? 'trend-positive' : 'trend-negative';
};

// --- STATS ---
const calculateStats = (data) => {
  let count = 0, totalPrice = 0, totalAvail = 0, totalRating = 0, validP = 0, validR = 0;
  
  if (!data) return { count: 0, avgPrice: 0, avgOcc: 0, avgRating: 0, validR: 0 };

  data.forEach(item => {
    const p = cleanPrice(item.price);
    if (p > 0) { totalPrice += p; validP++; }
    count++;
    const avail = item.availability_365 !== undefined ? item.availability_365 : 0;
    totalAvail += (365 - avail);
    if (item.review_scores_rating) { totalRating += parseFloat(item.review_scores_rating); validR++; }
  });

  const avgPrice = validP > 0 ? totalPrice / validP : 0;
  const avgOcc = count > 0 ? (totalAvail / (count * 365)) * 100 : 0;
  let avgRating = validR > 0 ? totalRating / validR : 0;
  if (avgRating > 5) avgRating = avgRating / 20;

  return { count, avgPrice, avgOcc, avgRating, validR };
};

const uniqueNeighborhoods = computed(() => {
  const hoods = new Set();
  rawListings.value.forEach(item => {
    const n = item.neighbourhood_cleansed || item.neighbourhood; 
    if (n) hoods.add(n);
  });
  return Array.from(hoods).sort();
});

// --- FILTROS ---
const filteredListings = computed(() => {
  return rawListings.value.filter(item => {
    const price = cleanPrice(item.price);
    if (price < appliedFilters.priceMin || price > appliedFilters.priceMax) return false;
    
    const n = item.neighbourhood_cleansed || item.neighbourhood;
    if (appliedFilters.neighborhood && n !== appliedFilters.neighborhood) return false;
    
    if (appliedFilters.propertyType && item.room_type !== appliedFilters.propertyType) return false;
    
    let rating = parseFloat(item.review_scores_rating || 0);
    if (rating > 5) rating = rating / 20; 
    if (rating < appliedFilters.minRating) return false;

    return true;
  });
});

// --- METRICS ---
const formattedMetrics = computed(() => {
  const currentStats = calculateStats(filteredListings.value);
  
  let trends = { count: 0, price: 0, occupancy: 0 };
  if (historyListings.value.length > 0) {
     const historyStats = calculateStats(historyListings.value);
     const calcTrend = (curr, hist) => hist > 0 ? ((curr - hist) / hist) * 100 : 0;
     trends = {
       count: calcTrend(currentStats.count, historyStats.count),
       price: calcTrend(currentStats.avgPrice, historyStats.avgPrice),
       occupancy: calcTrend(currentStats.avgOcc, historyStats.avgOcc)
     };
  }

  const displayPrice = currentStats.avgPrice * currentCurrencyInfo.value.rate;

  return {
    count: currentStats.count.toLocaleString(),
    price: Math.round(displayPrice),
    occupancy: Math.round(currentStats.avgOcc),
    rating: currentStats.avgRating.toFixed(2),
    reviewsCount: currentStats.validR.toLocaleString(),
    trends: {
      count: trends.count.toFixed(1),
      price: trends.price.toFixed(1),
      occupancy: trends.occupancy.toFixed(1)
    }
  };
});

const topNeighborhoods = computed(() => {
  const data = filteredListings.value;
  if (!data.length) return [];
  const stats = {}; 
  data.forEach(item => {
    const n = item.neighbourhood_cleansed || item.neighbourhood;
    if (!n) return;
    if (!stats[n]) stats[n] = { name: n, totalPrice: 0, count: 0, totalAvail: 0 };
    const p = cleanPrice(item.price);
    const avail = item.availability_365 !== undefined ? item.availability_365 : 0;
    if (p > 0) { stats[n].totalPrice += p; stats[n].count++; }
    stats[n].totalAvail += (365 - avail);
  });

  const result = Object.values(stats).map(hood => {
    const avgP = hood.count > 0 ? hood.totalPrice / hood.count : 0;
    const avgOcc = hood.count > 0 ? (hood.totalAvail / (hood.count * 365)) * 100 : 0;
    return {
      name: hood.name,
      price: Math.round(avgP * currentCurrencyInfo.value.rate),
      occupancy: Math.round(avgOcc)
    };
  });
  result.sort((a, b) => b.occupancy - a.occupancy); 
  return result.slice(0, 6); 
});

const activeTags = computed(() => {
  const tags = [];
  // Tag da Cidade (Não removível)
  /* Nota: Já está no template, não duplicar aqui */
  
  if (appliedFilters.neighborhood) tags.push({ key: 'neighborhood', label: 'Hood', value: appliedFilters.neighborhood });
  if (appliedFilters.propertyType) tags.push({ key: 'propertyType', label: 'Type', value: appliedFilters.propertyType });
  if (appliedFilters.priceMin > 0 || appliedFilters.priceMax < 1000) {
    tags.push({ key: 'priceRange', label: 'Price', value: `${currencySymbol.value}${appliedFilters.priceMin} - ${currencySymbol.value}${appliedFilters.priceMax}` });
  }
  if (appliedFilters.minRating > 1) {
    tags.push({ key: 'minRating', label: 'Rating', value: `${appliedFilters.minRating}+ ★` });
  }
  return tags;
});
</script>

<style scoped>
.explore-container {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 810px;
  color: black;
}

/* HEADER */
.header-section { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; }
.header-left { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.header-left h1 { font-weight: 800; font-size: 2rem; margin: 0; color: black; }
.header-actions { margin-top: 5px; }

/* BUTTONS & TAGS */
.filter-row { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; width: 100%; }
.filter-tags { display: contents; }
.filter-tag { display: flex; align-items: center; background-color: white; color: #FF5A5F; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; gap: 8px; white-space: nowrap; }
.city-tag { color: black; border: 1px solid lightgrey; }
.close-tag { background: none; border: none; color: #FF5A5F; font-size: 1.1rem; cursor: pointer; padding: 0; }
.clear-all-text { background: none; border: none; color: grey; text-decoration: underline; cursor: pointer; font-size: 0.85rem; white-space: nowrap; }

.btn-primary { background-color: #FF5A5F; color: white; border: none; padding: 10px 24px; border-radius: 30px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 10px rgba(255, 90, 95, 0.2); margin: 0; }
.btn-primary:hover { background-color: #e0484d; }
.btn-outline-primary { border: 2px solid #FF5A5F; color: #FF5A5F; background: transparent; padding: 8px 16px; border-radius: 20px; font-weight: 600; cursor: pointer; transition: background-color 0.2s; }
.btn-outline-primary:hover { background-color: rgba(255, 90, 95, 0.05); }

/* KPI CARDS (ESPALMADOS) */

.card {
  background: white;
  border-radius: 16px;
  padding: 0.5rem 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  border: 1px solid rgba(0,0,0,0.02);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 Colunas Fixas */
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.kpi-card h3 { font-size: 0.85rem; color: black; margin-bottom: 0.5rem; font-weight: 500; }
.kpi-value { font-size: 1.6rem; font-weight: 700; margin-bottom: 0.25rem; color: black; line-height: 1.2; }
.kpi-subtext { font-size: 0.75rem; font-weight: 600; margin-top: 0.2rem; }

/* Classes de Tendência */
.trend-positive { color: #10B981; }
.trend-negative { color: #FF5A5F; }

/* Estilos da Barra de Progresso (Pixel-Perfect) */
.progress-container {
  margin-top: 0.5rem; /* Espaço entre o valor e a barra */
  width: 100%;
  display: flex;
  align-items: center;
}

.progress-bar {
  width: 100%;
  height: 8px; /* Altura mais grossa como na imagem */
  background-color: lightgrey;
  border-radius: 9999px; /* Pílula perfeita */
  overflow: hidden;
  margin-top: 0.75rem;
}

.progress-fill {
  height: 100%;
  background-color: #FF5A5F; /* O teu vermelho oficial */
  border-radius: 9999px; /* Arredondar também a parte cheia */
  transition: width 0.5s ease-out; /* Animação suave ao carregar */
}

.star-color {
  color: gold;
}

/* MAP & CHARTS */
.heatmap-section { margin-bottom: 2rem; min-height: 400px; display: flex; flex-direction: column; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.toggle-switch { background: lightgrey; border-radius: 20px; padding: 4px; display: flex; }
.toggle-switch button { border: none; background: transparent; padding: 6px 16px; border-radius: 16px; cursor: pointer; font-size: 0.85rem; font-weight: 500; color: black; }
.toggle-switch button.active { background: #FF5A5F; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.map-placeholder { background-color: lightgrey; flex: 1; border-radius: 12px; display: flex; align-items: center; justify-content: center; }

.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem; }
.chart-card { min-height: 300px; display: flex; flex-direction: column; justify-content: space-between; }
.chart-placeholder { flex: 1; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; }
.simple-chart { width: 100%; height: 80px; opacity: 0.8; }
.chart-labels { display: flex; justify-content: space-between; width: 100%; padding: 0 10px; font-size: 0.7rem; color: grey; margin-top: 5px; }

/* TOP 6 CIRCLES */
.full-width-card { margin-bottom: 2rem; }
.circles-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; text-align: center; }
.circle-item { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; }
.circle-item h4 { margin: 0; font-size: 0.85rem; color: black; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px; }
.circle { width: 80px; height: 80px; border-radius: 50%; border: 4px solid #444; display: flex; align-items: center; justify-content: center; background: white; }
.circle-value { font-size: 1.1rem; font-weight: 700; color: #333; }
.circle-price { font-size: 0.9rem; color: #FF5A5F; font-weight: 700; }
.loading-text { text-align: center; color: grey; padding: 2rem; }

/* SIDEBAR */
.sidebar { position: fixed; top: 114px; left: -350px; width: 280px; height: calc(100vh - 106px); background-color: transparent; z-index: 900; overflow-y: auto; transition: left 0.3s ease-in-out; display: flex; flex-direction: column; }
.sidebar.open { left: 0; }
.sidebar-header { padding: 0 1.5rem 1.5rem 1.5rem; }
.sidebar-title { display: flex; align-items: center; gap: 10px; color: black; }
.sidebar-title h2 { margin: 0; font-size: 1.5rem; font-weight: 700; }
.sidebar-content { padding: 0rem 1.5rem; display: flex; flex-direction: column; gap: 1.5rem; }
.filter-group label { display: block; font-weight: 700; margin-bottom: 0.5rem; color: black; font-size: 0.95rem;}
.input-wrapper, .select-wrapper { position: relative; display: flex; align-items: center; }
.input-icon { position: absolute; left: 12px; color: grey; z-index: 1;}
.sidebar input[type="text"], .sidebar select { width: 100%; padding: 10px 12px 10px 36px; border: 1px solid lightgrey; border-radius: 12px; font-size: 0.9rem; color: black; outline: none; appearance: none; background: white; }
.sidebar select { cursor: pointer; background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22grey%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E"); background-repeat: no-repeat; background-position: right 1rem top 50%; background-size: 0.65rem auto; padding-right: 2rem; }
/* Filtro desativado (bairro quando muda cidade) */
.filter-group.disabled { opacity: 0.5; pointer-events: none; }

.multi-range-slider { position: relative; width: 100%; height: 30px; }
.slider-track { position: absolute; top: 12px; left: 0; width: 100%; height: 6px; background-color: lightgrey; border-radius: 5px; z-index: 0; }
.range-color { position: absolute; height: 100%; background-color: #FF5A5F; border-radius: 5px; z-index: 1; }
.multi-range-slider input[type="range"] { position: absolute; top: 0; left: 0; width: 100%; height: 30px; -webkit-appearance: none; pointer-events: none; background: transparent; z-index: 2; }
.multi-range-slider input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; pointer-events: all; width: 20px; height: 20px; border-radius: 50%; background: #FF5A5F; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.2); cursor: pointer; margin-top: 5px; }
.styled-slider { width: 100%; height: 6px; background: lightgrey; border-radius: 5px; outline: none; appearance: none; -webkit-appearance: none; }
.styled-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; border-radius: 50%; background: #FF5A5F; cursor: pointer; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.range-labels { display: flex; justify-content: space-between; font-size: 0.85rem; color: grey; margin-top: 5px;}
.date-buttons { display: flex; gap: 8px; margin-bottom: 10px; }
.date-btn { flex: 1; padding: 8px; font-size: 0.8rem; border: 1px solid lightgrey; border-radius: 8px; background: white; cursor: pointer; color: grey; }
.date-btn.active { background: #FF5A5F; color: white; border-color: #FF5A5F; }
.date-inputs { display: flex; gap: 10px; }
.date-inputs .input-wrapper { flex: 1; }
.date-inputs input { padding-left: 12px; }
.sidebar-footer { padding: 1.5rem; border-top: 1px solid transparent; display: flex; flex-direction: column; gap: 10px; margin-top: auto; }
.btn-apply { width: 100%; background: #FF5A5F; color: white; padding: 12px; border-radius: 12px; border: none; font-weight: 600; cursor: pointer; }
.btn-clear { width: 100%; background: white; color: black; padding: 12px; border-radius: 12px; border: 1px solid lightgrey; font-weight: 600; cursor: pointer; }
.loading-card, .error-card { background: white; padding: 2rem; border-radius: 16px; text-align: center; grid-column: 1 / -1; }
.error-card { border-left: 4px solid red; color: red; }
</style>