<template>
  <div class="explore-container">
    <div class="header-section">
      <div class="header-left">
        <h1>Explore Data</h1>
      </div>

      <div class="header-actions">
        <select
          v-model="selectedCity"
          @change="onCityChange"
          class="city-select"
        >
          <option value="porto">Porto</option>
          <option value="lisbon">Lisbon</option>
          <option value="barcelona">Barcelona</option>
        </select>

        <select
          v-model="selectedPeriod"
          @change="onPeriodChange"
          class="city-select"
        >
          <option v-for="p in store.PERIODS" :key="p.value" :value="p.value">
            {{ p.label }}
          </option>
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
        </div>

        <div class="card kpi-card">
          <h3>Avg. Price/Night ({{ currencySymbol }})</h3>
          <div class="kpi-value">
            {{ currencySymbol }}{{ formattedMetrics.price }}
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
      <h3>Top Neighbourhoods — Price & Occupancy</h3>

      <div v-if="topneighbourhoods.length > 0" class="circles-container">
        <div
          v-for="(item, index) in topneighbourhoods"
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
      <div v-else class="loading-text">Calculating neighbourhood data...</div>
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

const selectedCity = ref("porto");
const selectedPeriod = ref(store.state.period);
const heatmapMode = ref("Price");
const rawListings = shallowRef([]);
const historyData = ref([]);
const isLoading = ref(true);
const errorMessage = ref(null);

const onPeriodChange = () => {
  store.savePeriod(selectedPeriod.value);
  loadData();
};

const onCityChange = () => {
  selectedPeriod.value = "2025-09";
  store.savePeriod("2025-09");
  loadData();
};

const conversionRates = {
  USD: { rate: 1.0, symbol: "$" },
  EUR: { rate: 0.94, symbol: "€" },
  GBP: { rate: 0.82, symbol: "£" },
};

const currentCurrencyInfo = computed(
  () => conversionRates[store.state.currency] || conversionRates.USD
);
const currencySymbol = computed(() => currentCurrencyInfo.value.symbol);

const formatCityName = (val) =>
  val ? val.charAt(0).toUpperCase() + val.slice(1) : "";

const cleanPrice = (val) => {
  if (typeof val === "number") return val;
  if (!val) return 0;
  return parseFloat(String(val).replace(/[$,]/g, "")) || 0;
};

let abortController = null;

const loadData = async () => {
  if (abortController) abortController.abort();
  abortController = new AbortController();

  isLoading.value = true;
  errorMessage.value = null;
  rawListings.value = [];

  let cityKey = selectedCity.value.toLowerCase();
  if (cityKey === "lisboa") cityKey = "lisbon";

  const periodKey = selectedPeriod.value.replace("-", "_");
  const resourceName = `${cityKey}_${periodKey}_listings`;
  const historyName = `${cityKey}_history`;

  try {
    const [listingsRes, historyRes] = await Promise.all([
      fetch(`http://localhost:3000/${resourceName}`, {
        signal: abortController.signal,
      }),
      fetch(`http://localhost:3000/${historyName}`, {
        signal: abortController.signal,
      }),
    ]);

    if (!listingsRes.ok) throw new Error(`API Error (${listingsRes.status})`);

    const data = await listingsRes.json();
    rawListings.value = Object.freeze(data);

    if (historyRes.ok) {
      historyData.value = await historyRes.json();
    }
  } catch (err) {
    if (err.name !== "AbortError") {
      console.error(err);
      errorMessage.value = `Failed to load ${resourceName}. Check server.`;
    }
  } finally {
    if (!abortController.signal.aborted) {
      isLoading.value = false;
    }
  }
};

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

watch(heatmapMode, updateToggleGlider);

onMounted(() => {
  loadData();
  setTimeout(updateToggleGlider, 100);
});

onBeforeUnmount(() => {
  if (abortController) abortController.abort();
  rawListings.value = [];
});

const calculateStats = (data) => {
  if (!data)
    return { count: 0, avgPrice: 0, avgOcc: 0, avgRating: 0, validR: 0 };

  let count = 0,
    totalPrice = 0,
    totalAvail = 0,
    totalRating = 0,
    validP = 0,
    validR = 0;

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

const trendData = computed(() => {
  if (!historyData.value.length) return [];
  return historyData.value.map((h) => ({
    label: h.label,
    price: h.avgPrice * currentCurrencyInfo.value.rate,
    occupancy: h.occupancyRate,
  }));
});

const chartLabels = computed(() => trendData.value.map((d) => d.label));
const chartPrices = computed(() => trendData.value.map((d) => d.price));
const chartOccupancy = computed(() => trendData.value.map((d) => d.occupancy));

const mapCenter = computed(() => {
  if (selectedCity.value === "porto") return [41.1579, -8.6291];
  if (selectedCity.value === "lisbon") return [38.7223, -9.1393];
  if (selectedCity.value === "barcelona") return [41.3851, 2.1734];
  return [41.1579, -8.6291];
});

const topneighbourhoods = computed(() => {
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
/* LAYOUT */
.explore-container {
  width: 100%;
  max-width: 1000px;
  padding: 2rem 1rem;
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
  font-size: 2rem;
  font-weight: 800;
  color: black;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 5px;
}

.city-select {
  margin-top: 5px;
  padding: 10px 24px;
  font-weight: 600;
  color: black;
  background-color: #fff;
  border: none;
  border-radius: 9999px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: pointer;
}

.city-select:hover {
  border-color: #ff5a5f;
}

.city-select:focus {
  border-color: #ff5a5f;
  box-shadow: 0 2px 12px rgba(255, 90, 95, 0.15);
}

.btn-primary {
  margin-top: 5px;
  padding: 10px 24px;
  font-weight: 600;
  color: white;
  background-color: #ff5a5f;
  border: none;
  border-radius: 9999px;
  box-shadow: 0 4px 10px rgba(255, 90, 95, 0.2);
  cursor: pointer;
}

/* CARDS */
.card {
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.02);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
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

.star-color {
  color: gold;
}

/* PROGRESS BAR */
.progress-bar {
  height: 8px;
  margin-top: 5px;
  overflow: hidden;
  background-color: rgb(234, 234, 234);
  border-radius: 9999px;
}

.progress-fill {
  height: 100%;
  background-color: #ff5a5f;
  border-radius: 9999px;
  transition: width 0.5s ease-out;
}

/* MAP SECTION */
.heatmap-section {
  display: flex;
  flex-direction: column;
  height: 500px;
  margin-bottom: 2rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.toggle-switch {
  position: relative;
  display: flex;
  padding: 4px;
  background: rgb(234, 234, 234);
  border-radius: 20px;
  isolation: isolate;
}

.toggle-glider {
  position: absolute;
  top: 4px;
  left: 0;
  z-index: 1;
  background-color: #ff5a5f;
  border-radius: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toggle-switch button {
  position: relative;
  z-index: 2;
  padding: 6px 16px;
  font-size: 0.85rem;
  font-weight: 500;
  color: black;
  background: transparent;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: color 0.3s ease;
}

.toggle-switch button.active {
  color: white;
  background: transparent;
  box-shadow: none;
}

.map-placeholder {
  position: relative;
  flex: 1;
  overflow: hidden;
  background-color: lightgrey;
  border-radius: 12px;
}

/* CHARTS GRID */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 300px;
}

.chart-placeholder {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  flex: 1;
  width: 100%;
  height: 100%;
}

.circles-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
  margin-bottom: 4rem;
  text-align: center;
}

.circle-item {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 0.5rem;
  height: 100%;
}

.circle-item h4 {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 6rem;
  margin: 0;
  font-size: 0.85rem;
  font-weight: 600;
  color: black;
  text-align: center;
  white-space: normal;
}

.circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: white;
  border: 4px solid black;
  border-radius: 50%;
}

.circle-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
}

.circle-price {
  font-size: 0.9rem;
  font-weight: 700;
  color: #ff5a5f;
}

/* STATES */
.loading-text {
  padding: 2rem;
  color: grey;
  text-align: center;
}

.loading-card {
  grid-column: 1 / -1;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  text-align: center;
}

.error-card {
  grid-column: 1 / -1;
  padding: 2rem;
  color: red;
  background: white;
  border-left: 4px solid red;
  border-radius: 16px;
  text-align: center;
}

.no-data {
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: grey;
}
</style>
