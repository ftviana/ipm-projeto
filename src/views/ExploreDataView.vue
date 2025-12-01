<template>
  <div class="explore-container">
    <div class="header-section">
      <div class="header-left">
        <h1>Explore Data</h1>
      </div>

      <div class="header-actions">
        <select v-model="selectedCity" @change="loadData" class="city-select">
          <option value="porto">Porto</option>
          <option value="lisbon">Lisbon</option>
          <option value="barcelona">Barcelona</option>
        </select>

        <button class="btn-primary" @click="router.push('/export')">
          Generate Report
        </button>
      </div>
    </div>

    <div class="kpi-grid">
      <div v-if="isLoading" class="loading-card full-width">
        <p>Loading data...</p>
      </div>

      <div v-else-if="errorMessage" class="error-card full-width">
        <p>⚠️ {{ errorMessage }}</p>
      </div>

      <template v-else>
        <div class="card kpi-card">
          <h3>Active Listings</h3>
          <div class="kpi-value">{{ formattedMetrics.count }}</div>
          <div class="kpi-subtext trend-positive">
            <span>↑</span> 5.2% vs last year
          </div>
        </div>

        <div class="card kpi-card">
          <h3>Avg. Price/Night ({{ currencySymbol }})</h3>
          <div class="kpi-value">
            {{ currencySymbol }}{{ formattedMetrics.price }}
          </div>
          <div class="kpi-subtext trend-negative">
            <span>↓</span> 1.2% vs last year
          </div>
        </div>

        <div class="card kpi-card">
          <h3>Occupancy Rate (%)</h3>
          <div class="kpi-value">{{ formattedMetrics.occupancy }}%</div>
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: formattedMetrics.occupancy + '%' }"
            ></div>
          </div>
        </div>

        <div class="card kpi-card">
          <h3>Avg. Rating (★)</h3>
          <div class="kpi-value">
            {{ formattedMetrics.rating }}
            <span class="star-color">★</span>
          </div>
          <div class="kpi-subtext">
            Based on {{ formattedMetrics.reviewsCount }} reviews
          </div>
        </div>
      </template>
    </div>

    <div class="card heatmap-section">
      <div class="card-header">
        <h3>Geospatial Heatmap — {{ formatCityName(selectedCity) }}</h3>

        <div class="toggle-switch" ref="toggleContainer">
          <span class="toggle-glider" ref="toggleGlider"></span>

          <button
            :class="{ active: heatmapMode === 'Price' }"
            @click="heatmapMode = 'Price'"
          >
            Price
          </button>
          <button
            :class="{ active: heatmapMode === 'Occupancy' }"
            @click="heatmapMode = 'Occupancy'"
          >
            Occupancy
          </button>
        </div>
      </div>

      <div class="map-placeholder" style="background: none">
        <HeatmapMap
          v-if="!isLoading && rawListings.length > 0"
          :listings="rawListings"
          :center="mapCenter"
          :mode="heatmapMode"
        />
        <div v-else-if="isLoading" style="color: grey">Loading Map...</div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h3>Avg. Price</h3>
        <div class="chart-placeholder">
          <TrendChart
            v-if="!isLoading && chartPrices.length > 0"
            :labels="chartLabels"
            :values="chartPrices"
            label="Avg Price"
            color="#FF5A5F"
          />
          <p v-else class="no-data">No trend data available</p>
        </div>
      </div>

      <div class="card chart-card">
        <h3>Occupancy Trend</h3>
        <div class="chart-placeholder">
          <TrendChart
            v-if="!isLoading && chartOccupancy.length > 0"
            :labels="chartLabels"
            :values="chartOccupancy"
            label="Occupancy"
            color="#333"
          />
          <p v-else class="no-data">No trend data available</p>
        </div>
      </div>
    </div>

    <div class="card full-width-card">
      <h3>Top Neighborhoods — Price & Occupancy</h3>

      <div v-if="topNeighborhoods.length > 0" class="circles-container">
        <div
          v-for="(item, index) in topNeighborhoods"
          :key="index"
          class="circle-item"
        >
          <h4>{{ item.name }}</h4>
          <div class="circle">
            <span class="circle-value">{{ item.occupancy }}%</span>
          </div>
          <span class="circle-price">{{ currencySymbol }}{{ item.price }}</span>
        </div>
      </div>
      <div v-else class="loading-text">Calculating neighborhood data...</div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  shallowRef,
  computed,
  onMounted,
  onBeforeUnmount,
  watch,
  nextTick,
} from "vue";
import { store } from "../store.js";
import { useRouter } from "vue-router";
import TrendChart from "../components/TrendChart.vue";
import HeatmapMap from "../components/HeatmapMap.vue";

const router = useRouter();

// --- STATE ---
const selectedCity = ref("porto");
const heatmapMode = ref("Price");
const rawListings = shallowRef([]);
const isLoading = ref(true);
const errorMessage = ref(null);

// --- CURRENCY ---
const conversionRates = {
  USD: { rate: 1.0, symbol: "$" },
  EUR: { rate: 0.94, symbol: "€" },
  GBP: { rate: 0.82, symbol: "£" },
};

const currentCurrencyInfo = computed(
  () => conversionRates[store.state.currency] || conversionRates.USD
);
const currencySymbol = computed(() => currentCurrencyInfo.value.symbol);

// --- HELPERS ---
const formatCityName = (val) =>
  val ? val.charAt(0).toUpperCase() + val.slice(1) : "";

const cleanPrice = (val) => {
  if (typeof val === "number") return val;
  if (!val) return 0;
  return parseFloat(String(val).replace(/[$,]/g, "")) || 0;
};

// --- DATA LOADING ---
let abortController = null;

const loadData = async () => {
  if (abortController) abortController.abort();
  abortController = new AbortController();

  isLoading.value = true;
  errorMessage.value = null;
  rawListings.value = [];

  let cityKey = selectedCity.value.toLowerCase();
  if (cityKey === "lisboa") cityKey = "lisbon";

  const resourceName = `${cityKey}_listings`;

  try {
    const response = await fetch(`http://localhost:3000/${resourceName}`, {
      signal: abortController.signal,
    });

    if (!response.ok) throw new Error(`API Error (${response.status})`);

    const data = await response.json();

    rawListings.value = Object.freeze(data);
  } catch (err) {
    if (err.name === "AbortError") {
      console.log("Fetch cancelled");
    } else {
      console.error(err);
      errorMessage.value = `Failed to load ${resourceName}. Check server.`;
    }
  } finally {
    if (!abortController.signal.aborted) {
      isLoading.value = false;
    }
  }
};

// --- GLIDER LOGIC ---
const toggleContainer = ref(null);
const toggleGlider = ref(null);

const updateToggleGlider = async () => {
  await nextTick();
  if (!toggleContainer.value || !toggleGlider.value) return;
  const activeButton = toggleContainer.value.querySelector(".active");
  if (activeButton) {
    const { offsetLeft, offsetWidth, offsetHeight } = activeButton;
    toggleGlider.value.style.width = `${offsetWidth}px`;
    toggleGlider.value.style.height = `${offsetHeight}px`;
    toggleGlider.value.style.transform = `translateX(${offsetLeft}px)`;
  }
};

watch(heatmapMode, () => {
  updateToggleGlider();
});

onMounted(() => {
  loadData();
  setTimeout(() => updateToggleGlider(), 100);
});

// CLEANUP ON EXIT
onBeforeUnmount(() => {
  if (abortController) abortController.abort();
  rawListings.value = [];
});

// --- STATISTICS ---
const calculateStats = (data) => {
  let count = 0,
    totalPrice = 0,
    totalAvail = 0,
    totalRating = 0,
    validP = 0,
    validR = 0;

  if (!data)
    return { count: 0, avgPrice: 0, avgOcc: 0, avgRating: 0, validR: 0 };

  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    const p = cleanPrice(item.price);
    if (p > 0) {
      totalPrice += p;
      validP++;
    }
    count++;

    const avail = parseInt(item.availability_365) || 0;
    totalAvail += 365 - avail;

    if (item.review_scores_rating) {
      totalRating += parseFloat(item.review_scores_rating);
      validR++;
    }
  }

  const avgPrice = validP > 0 ? totalPrice / validP : 0;
  const avgOcc = count > 0 ? (totalAvail / (count * 365)) * 100 : 0;
  let avgRating = validR > 0 ? totalRating / validR : 0;
  if (avgRating > 5) avgRating = avgRating / 20;

  return { count, avgPrice, avgOcc, avgRating, validR };
};

const formattedMetrics = computed(() => {
  const stats = calculateStats(rawListings.value);
  const displayPrice = stats.avgPrice * currentCurrencyInfo.value.rate;

  return {
    count: stats.count.toLocaleString(),
    price: Math.round(displayPrice),
    occupancy: Math.round(stats.avgOcc),
    rating: stats.avgRating.toFixed(2),
    reviewsCount: stats.validR.toLocaleString(),
  };
});

// --- TRENDS ---
const trendData = computed(() => {
  if (!rawListings.value.length) return [];

  const groups = {};

  for (let i = 0; i < rawListings.value.length; i++) {
    const item = rawListings.value[i];
    if (!item.last_review) continue;
    const dateKey = item.last_review.substring(0, 7);

    if (!groups[dateKey]) {
      groups[dateKey] = { priceSum: 0, availSum: 0, count: 0 };
    }

    groups[dateKey].priceSum += cleanPrice(item.price);
    const avail = parseInt(item.availability_365) || 0;
    groups[dateKey].availSum += 365 - avail;
    groups[dateKey].count++;
  }

  const sortedKeys = Object.keys(groups).sort().slice(-6);

  return sortedKeys.map((key) => {
    const g = groups[key];
    const dateObj = new Date(key + "-01");
    const label = dateObj.toLocaleString("en-US", { month: "short" });

    return {
      label: label,
      price: (g.priceSum / g.count) * currentCurrencyInfo.value.rate,
      occupancy: (g.availSum / g.count / 365) * 100,
    };
  });
});

const chartLabels = computed(() => trendData.value.map((d) => d.label));
const chartPrices = computed(() => trendData.value.map((d) => d.price));
const chartOccupancy = computed(() => trendData.value.map((d) => d.occupancy));

// --- MAP CENTER ---
const mapCenter = computed(() => {
  if (selectedCity.value === "porto") return [41.1579, -8.6291];
  if (selectedCity.value === "lisbon") return [38.7223, -9.1393];
  if (selectedCity.value === "barcelona") return [41.3851, 2.1734];
  return [41.1579, -8.6291];
});

// --- TOP NEIGHBORHOODS ---
const topNeighborhoods = computed(() => {
  const data = rawListings.value;
  if (!data.length) return [];
  const stats = {};

  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    const n = item.neighbourhood_cleansed || item.neighbourhood;
    if (!n) continue;

    if (!stats[n])
      stats[n] = { name: n, totalPrice: 0, count: 0, totalAvail: 0 };
    const p = cleanPrice(item.price);
    const avail = parseInt(item.availability_365) || 0;

    if (p > 0) {
      stats[n].totalPrice += p;
      stats[n].count++;
    }
    stats[n].totalAvail += 365 - avail;
  }

  const result = Object.values(stats).map((hood) => {
    const avgP = hood.count > 0 ? hood.totalPrice / hood.count : 0;
    const avgOcc =
      hood.count > 0 ? (hood.totalAvail / (hood.count * 365)) * 100 : 0;
    return {
      name: hood.name,
      price: Math.round(avgP * currentCurrencyInfo.value.rate),
      occupancy: Math.round(avgOcc),
    };
  });
  result.sort((a, b) => b.occupancy - a.occupancy);
  return result.slice(0, 6);
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

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.header-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.header-left h1 {
  font-weight: 800;
  font-size: 2rem;
  color: black;
}

.header-actions {
  margin-top: 5px;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.city-select {
  background-color: transparent;
  color: black;
  border: none;
  padding: 10px 24px;
  border-radius: 9999px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  text-align-last: center;
  outline: none;
  font-size: 0.9rem;
}

.btn-primary {
  margin-top: 5px;
  background-color: #ff5a5f;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 9999px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(255, 90, 95, 0.2);
}

/* CARDS */

.card {
  background: white;
  border-radius: 16px;
  padding: 0.5rem 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.02);
}

/* KPI GRID */

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.kpi-card h3 {
  font-size: 0.85rem;
  font-weight: 500;
  color: dimgrey;
}

.kpi-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: black;
}

.kpi-subtext {
  font-size: 0.6rem;
  font-weight: 500;
  color: dimgrey;
}

.trend-positive {
  color: #10b981;
}

.trend-negative {
  color: #ff5a5f;
}

/* PROGRESS BAR */

.progress-bar {
  margin-top: 5px;
  height: 8px;
  background-color: rgb(234, 234, 234);
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #ff5a5f;
  border-radius: 9999px;
  transition: width 0.5s ease-out;
}

.star-color {
  color: gold;
}

/* MAP SECTION */

.heatmap-section {
  margin-bottom: 2rem;
  height: 500px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

/* --- TOGGLE SWITCH COM GLIDER --- */
.toggle-switch {
  position: relative; /* Necessário para o glider absoluto */
  background: rgb(234, 234, 234);
  border-radius: 20px;
  padding: 4px;
  display: flex;
  isolation: isolate; /* Cria novo contexto de empilhamento */
}

.toggle-glider {
  position: absolute;
  top: 4px; /* Igual ao padding do pai */
  left: 0;
  background-color: #ff5a5f; /* Cor Vermelha */
  border-radius: 16px; /* Igual ao botão */
  z-index: 1; /* Fica atrás do texto */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* A animação de deslize */
  /* Largura e altura são definidas via JS */
}

.toggle-switch button {
  position: relative;
  z-index: 2; /* Texto fica por cima do glider */
  border: none;
  background: transparent; /* Transparente para ver o glider por trás */
  padding: 6px 16px;
  border-radius: 16px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: black;
  transition: color 0.3s ease; /* Transição suave da cor do texto */
}

.toggle-switch button.active {
  color: white; /* Texto fica branco quando o glider está por baixo */
  background: transparent;
  box-shadow: none;
}

.map-placeholder {
  background-color: lightgrey;
  flex: 1;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

/* CHARTS GRID */

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chart-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
  height: 100%;
  position: relative;
}

.simple-chart {
  width: 100%;
  height: 80px;
  opacity: 0.8;
}

/* TOP NEIGHBORHOODS */

.full-width-card {
  margin-bottom: 2rem;
}

.circles-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
  text-align: center;
}

.circle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  height: 100%;
  justify-content: flex-start;
}

/* --- FIXED: NAME ALIGNMENT --- */
.circle-item h4 {
  margin: 0;
  font-size: 0.85rem;
  color: black;
  font-weight: 600;
  white-space: normal;
  text-align: center;

  /* Force height for ~3 lines of text to align balls below */
  min-height: 6rem;
  display: flex;
  align-items: center; /* Center text vertically in the fixed space */
  justify-content: center;
}

.circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid black;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
}

.circle-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
}

.circle-price {
  font-size: 0.9rem;
  color: #ff5a5f;
  font-weight: 700;
}

/* STATES */

.loading-text {
  text-align: center;
  color: grey;
  padding: 2rem;
}

.loading-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  grid-column: 1 / -1;
}

.error-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  grid-column: 1 / -1;
  border-left: 4px solid red;
  color: red;
}

.no-data {
  color: grey;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}
</style>
