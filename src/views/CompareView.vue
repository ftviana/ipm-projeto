<template>
  <div class="compare-container">
    <div class="header-section">
      <div class="header-left">
        <h1>Cities</h1>
      </div>
    </div>

    <div class="selectors-row">
      <div class="select-group">
        <label>City A</label>
        <select v-model="cityA" class="city-select city-a-select">
          <option value="porto">Porto</option>
          <option value="lisbon">Lisbon</option>
          <option value="barcelona">Barcelona</option>
        </select>
        <select v-model="periodA" class="city-select period-select">
          <option v-for="p in store.PERIODS" :key="p.value" :value="p.value">
            {{ p.label }}
          </option>
        </select>
      </div>

      <div class="select-group">
        <label>City B</label>
        <select v-model="cityB" class="city-select city-b-select">
          <option value="porto">Porto</option>
          <option value="lisbon">Lisbon</option>
          <option value="barcelona">Barcelona</option>
        </select>
        <select v-model="periodB" class="city-select period-select">
          <option v-for="p in store.PERIODS" :key="p.value" :value="p.value">
            {{ p.label }}
          </option>
        </select>
      </div>

      <button
        class="btn-primary"
        @click="fetchComparisonData"
        :disabled="isLoading"
      >
        {{ isLoading ? "Loading..." : "Compare" }}
      </button>
    </div>
  </div>

  <div v-if="hasData" class="comparison-content">
    <div class="insight-banner">
      <h3>{{ insightText }}</h3>
    </div>

    <div class="stats-grid">
      <div class="city-card card-a">
        <div class="card-header-a">
          <h2>{{ displayNameA }}</h2>
          <span v-if="!isSameCity" class="period-label">{{
            getPeriodLabel(comparedPeriodA)
          }}</span>
        </div>
        <div class="card-body">
          <div class="stat-row">
            <span>Avg. Price</span>
            <strong>{{ currencySymbol }}{{ statsA.price }}</strong>
          </div>
          <div class="stat-row">
            <span>Occupancy</span>
            <strong>{{ statsA.occupancy }}%</strong>
          </div>
          <div class="stat-row">
            <span>Listings</span>
            <strong>{{ statsA.count }}</strong>
          </div>
          <div class="stat-row">
            <span>Rating</span>
            <strong>{{ statsA.rating }} ★</strong>
          </div>
        </div>
      </div>

      <div class="city-card card-b">
        <div class="card-header-b">
          <h2>{{ displayNameB }}</h2>
          <span v-if="!isSameCity" class="period-label">{{
            getPeriodLabel(comparedPeriodB)
          }}</span>
        </div>
        <div class="card-body">
          <div class="stat-row">
            <span>Avg. Price</span>
            <strong>{{ currencySymbol }}{{ statsB.price }}</strong>
          </div>
          <div class="stat-row">
            <span>Occupancy</span>
            <strong>{{ statsB.occupancy }}%</strong>
          </div>
          <div class="stat-row">
            <span>Listings</span>
            <strong>{{ statsB.count }}</strong>
          </div>
          <div class="stat-row">
            <span>Rating</span>
            <strong>{{ statsB.rating }} ★</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="chart-section card">
      <div class="chart-header">
        <h3>
          Trend Comparison: {{ formatCityName(cityA) }} vs.
          {{ formatCityName(cityB) }}
        </h3>
        <div class="chart-controls">
          <button
            :class="{ active: chartType === 'bar' }"
            @click="chartType = 'bar'"
          >
            Bar
          </button>
          <button
            :class="{ active: chartType === 'line' }"
            @click="chartType = 'line'"
          >
            Line
          </button>
        </div>
      </div>

      <div class="chart-wrapper">
        <Bar
          v-if="chartType === 'bar'"
          :data="chartData"
          :options="chartOptions"
        />
        <Line v-else :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>

  <div v-else-if="!isLoading" class="empty-state"></div>
</template>

<script setup>
import { ref, computed, reactive } from "vue";
import { store } from "../store.js";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar, Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const cityA = ref("porto");
const cityB = ref("lisbon");
const periodA = ref(store.state.period);
const periodB = ref(store.state.period);
const isLoading = ref(false);
const hasData = ref(false);
const chartType = ref("bar");

const comparedCityA = ref("");
const comparedCityB = ref("");
const comparedPeriodA = ref("");
const comparedPeriodB = ref("");

const statsA = reactive({ price: 0, occupancy: 0, count: 0, rating: 0 });
const statsB = reactive({ price: 0, occupancy: 0, count: 0, rating: 0 });

const currencySymbol = computed(() =>
  store.state.currency === "EUR"
    ? "€"
    : store.state.currency === "GBP"
    ? "£"
    : "$"
);
const conversionRate = computed(() =>
  store.state.currency === "EUR"
    ? 0.94
    : store.state.currency === "GBP"
    ? 0.82
    : 1.0
);

const formatCityName = (val) =>
  val ? val.charAt(0).toUpperCase() + val.slice(1) : "";

const getPeriodLabel = (period) => {
  const p = store.PERIODS.find((x) => x.value === period);
  return p ? p.label : period;
};

const getShortPeriod = (period) => {
  const p = store.PERIODS.find((x) => x.value === period);
  return p ? p.label.replace(" 2025", "") : period;
};

const isSameCity = computed(
  () =>
    comparedCityA.value === comparedCityB.value && comparedCityA.value !== ""
);

const displayNameA = computed(() => {
  if (!comparedCityA.value) return "";
  if (isSameCity.value) {
    return `${formatCityName(comparedCityA.value)} (${getShortPeriod(
      comparedPeriodA.value
    )})`;
  }
  return formatCityName(comparedCityA.value);
});

const displayNameB = computed(() => {
  if (!comparedCityB.value) return "";
  if (isSameCity.value) {
    return `${formatCityName(comparedCityB.value)} (${getShortPeriod(
      comparedPeriodB.value
    )})`;
  }
  return formatCityName(comparedCityB.value);
});

const cleanPrice = (val) => parseFloat(String(val).replace(/[$,]/g, "")) || 0;

const calculateCityStats = (data) => {
  let count = 0,
    totalPrice = 0,
    totalAvail = 0,
    totalRating = 0,
    validR = 0;

  data.forEach((item) => {
    const p = cleanPrice(item.price);
    totalPrice += p;
    count++;
    const avail = parseInt(item.availability_365) || 0;
    totalAvail += 365 - avail;
    if (item.review_scores_rating) {
      let r = parseFloat(item.review_scores_rating);
      if (r > 5) r /= 20;
      totalRating += r;
      validR++;
    }
  });

  return {
    count: count.toLocaleString(),
    price: Math.round(
      (count > 0 ? totalPrice / count : 0) * conversionRate.value
    ),
    occupancy: Math.round(count > 0 ? (totalAvail / (count * 365)) * 100 : 0),
    rating: validR > 0 ? (totalRating / validR).toFixed(2) : 0,
  };
};

const fetchComparisonData = async () => {
  if (cityA.value === cityB.value && periodA.value === periodB.value)
    return alert("Please select different cities or periods to compare.");
  isLoading.value = true;
  hasData.value = false;

  try {
    const periodKeyA = periodA.value.replace("-", "_");
    const periodKeyB = periodB.value.replace("-", "_");
    const [resA, resB] = await Promise.all([
      fetch(
        `http://localhost:3000/${cityA.value.toLowerCase()}_${periodKeyA}_listings`
      ),
      fetch(
        `http://localhost:3000/${cityB.value.toLowerCase()}_${periodKeyB}_listings`
      ),
    ]);
    if (!resA.ok || !resB.ok) throw new Error("Failed to fetch data");
    const dataA = await resA.json();
    const dataB = await resB.json();
    Object.assign(statsA, calculateCityStats(dataA));
    Object.assign(statsB, calculateCityStats(dataB));
    comparedCityA.value = cityA.value;
    comparedCityB.value = cityB.value;
    comparedPeriodA.value = periodA.value;
    comparedPeriodB.value = periodB.value;
    hasData.value = true;
  } catch (error) {
    console.error(error);
    alert("Error loading data. Check if server is running.");
  } finally {
    isLoading.value = false;
  }
};

const insightText = computed(() => {
  if (!hasData.value) return "";
  const diff = statsA.price - statsB.price;
  const pDiff = Math.abs(Math.round((diff / statsB.price) * 100));
  if (diff > 0)
    return `${displayNameA.value} has +${pDiff}% average price vs ${displayNameB.value}`;
  if (diff < 0)
    return `${displayNameB.value} has +${pDiff}% average price vs ${displayNameA.value}`;
  return "Both have similar average prices.";
});

const chartData = computed(() => ({
  labels: ["Avg. Price", "Occupancy Rate", "Rating"],
  datasets: [
    {
      label: displayNameA.value,
      backgroundColor: "#FF5A5F",
      borderColor: "#FF5A5F",
      data: [statsA.price, statsA.occupancy, parseFloat(statsA.rating) * 20],
      borderRadius: 6,
    },
    {
      label: displayNameB.value,
      backgroundColor: "#32A9E1",
      borderColor: "#32A9E1",
      data: [statsB.price, statsB.occupancy, parseFloat(statsB.rating) * 20],
      borderRadius: 6,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: "top" },
    tooltip: { mode: "index", intersect: false },
  },
  scales: {
    y: { beginAtZero: true, grid: { color: "#f0f0f0" } },
    x: { grid: { display: false } },
  },
};
</script>

<style scoped>
/* LAYOUT */
.compare-container {
  width: 100%;
  max-width: 1000px;
  padding: 2rem 1rem;
  color: black;
}

.header-section {
  margin-bottom: 2rem;
}

/* HEADER */
.header-section h1 {
  margin: 0 0 1.5rem 0;
  font-size: 2rem;
  font-weight: 800;
  color: black;
}

/* SELECTORS ROW */
.selectors-row {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.select-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex: 1;
  gap: 0.5rem;
}

.select-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: grey;
}

.city-select {
  width: 100%;
  padding: 15px 12px;
  font-size: 0.85rem;
  font-weight: 600;
  color: black;
  border: none;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
}

.period-select {
  margin-top: 0.5rem;
  padding: 15px 12px;
  font-size: 0.85rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.btn-primary {
  align-self: flex-start;
  margin-top: 1.9rem;
  padding: 15px 24px;
  font-weight: 600;
  color: white;
  background-color: black;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #333;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* INSIGHT BANNER */
.insight-banner {
  margin-bottom: 2rem;
  padding: 1rem;
  color: white;
  text-align: center;
  background: linear-gradient(90deg, #ff5a5f 0%, #32a9e1 100%);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.insight-banner h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

/* STATS GRID */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.city-card {
  overflow: hidden;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.02);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.card-header-a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background-color: rgba(255, 90, 95, 0.1);
  border-bottom: 2px solid #32a9e1;
}

.card-header-b {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background-color: rgba(50, 169, 225, 0.1);
  border-bottom: 2px solid #ff5a5f;
}

.period-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #666;
  background: rgba(0, 0, 0, 0.05);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.city-card h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
}

.card-body {
  padding: 1.5rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.stat-row:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.stat-row span {
  font-size: 0.9rem;
  color: grey;
}

.stat-row strong {
  font-size: 1.1rem;
  font-weight: 700;
}

/* CHART SECTION */
.chart-section {
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.chart-controls button {
  padding: 6px 12px;
  font-size: 0.85rem;
  background: white;
  border: 1px solid lightgrey;
  cursor: pointer;
}

.chart-controls button:first-child {
  border-radius: 6px 0 0 6px;
}

.chart-controls button:last-child {
  border-left: none;
  border-radius: 0 6px 6px 0;
}

.chart-controls button.active {
  color: white;
  background-color: black;
  border-color: black;
}

.chart-wrapper {
  height: 350px;
}

/* STATES */
.empty-state {
  margin-top: 3rem;
  color: grey;
  font-style: italic;
  text-align: center;
}
</style>
