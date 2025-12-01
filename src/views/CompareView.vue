<template>
  <div class="compare-container">
    <div class="header-section">
      <h1>Compare Cities</h1>

      <div class="selectors-row">
        <div class="select-group">
          <label>City A</label>
          <select v-model="cityA" class="city-select city-a-select">
            <option value="porto">Porto</option>
            <option value="lisbon">Lisbon</option>
            <option value="barcelona">Barcelona</option>
          </select>
        </div>

        <div class="vs-badge">VS</div>

        <div class="select-group">
          <label>City B</label>
          <select v-model="cityB" class="city-select city-b-select">
            <option value="porto">Porto</option>
            <option value="lisbon">Lisbon</option>
            <option value="barcelona">Barcelona</option>
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
            <h2>{{ formatCityName(cityA) }}</h2>
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
            <h2>{{ formatCityName(cityB) }}</h2>
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
  </div>
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
const isLoading = ref(false);
const hasData = ref(false);
const chartType = ref("bar");

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
  if (cityA.value === cityB.value)
    return alert("Please select two different cities to compare.");
  isLoading.value = true;
  hasData.value = false;

  try {
    const [resA, resB] = await Promise.all([
      fetch(`http://localhost:3000/${cityA.value.toLowerCase()}_listings`),
      fetch(`http://localhost:3000/${cityB.value.toLowerCase()}_listings`),
    ]);
    if (!resA.ok || !resB.ok) throw new Error("Failed to fetch data");
    const dataA = await resA.json();
    const dataB = await resB.json();
    Object.assign(statsA, calculateCityStats(dataA));
    Object.assign(statsB, calculateCityStats(dataB));
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
    return `${formatCityName(
      cityA.value
    )} has +${pDiff}% average price vs ${formatCityName(cityB.value)}`;
  if (diff < 0)
    return `${formatCityName(
      cityB.value
    )} has +${pDiff}% average price vs ${formatCityName(cityA.value)}`;
  return "Both cities have similar average prices.";
});

const chartData = computed(() => ({
  labels: ["Avg. Price", "Occupancy (%)", "Rating (x20)", "Listings (/10)"],
  datasets: [
    {
      label: formatCityName(cityA.value),
      backgroundColor: "#FF5A5F",
      borderColor: "#FF5A5F",
      data: [
        statsA.price,
        statsA.occupancy,
        statsA.rating * 20,
        statsA.count.replace(/,/g, "") / 10,
      ],
      borderRadius: 6,
    },
    {
      label: formatCityName(cityB.value),
      backgroundColor: "#32A9E1",
      borderColor: "#32A9E1",
      data: [
        statsB.price,
        statsB.occupancy,
        statsB.rating * 20,
        statsB.count.replace(/,/g, "") / 10,
      ],
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
.compare-container {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 1000px;
  color: black;
}

.header-section h1 {
  font-weight: 800;
  font-size: 2rem;
  margin: 0 0 1.5rem 0;
  color: black;
}

.selectors-row {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 1rem;
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.select-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  flex: 1;
}

.select-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: grey;
}

.city-select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: black;
  border: none;
  cursor: pointer;
}

.vs-badge {
  font-weight: 800;
  color: lightgrey;
  font-size: 1.2rem;
  padding-bottom: 10px;
}

.btn-primary {
  background-color: black;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  height: 42px;
}

.btn-primary:hover {
  background-color: #333;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.insight-banner {
  background: linear-gradient(90deg, #ff5a5f 0%, #32a9e1 100%);
  color: white;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.insight-banner h3 {
  margin: 0;
  font-weight: 600;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.city-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.02);
}

.card-header-a {
  background-color: rgba(255, 90, 95, 0.1);
  padding: 1rem 1.5rem;
  border-bottom: 2px solid #32a9e1;
}

.card-header-b {
  background-color: rgba(50, 169, 225, 0.1);
  padding: 1rem 1.5rem;
  border-bottom: 2px solid #ff5a5f;
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
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.stat-row span {
  color: grey;
  font-size: 0.9rem;
}

.stat-row strong {
  font-size: 1.1rem;
  font-weight: 700;
}

.chart-section {
  background: white;
  padding: 2rem;
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
  background: white;
  border: 1px solid lightgrey;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 0.85rem;
}

.chart-controls button:first-child {
  border-radius: 6px 0 0 6px;
}

.chart-controls button:last-child {
  border-radius: 0 6px 6px 0;
  border-left: none;
}

.chart-controls button.active {
  background-color: black;
  color: white;
  border-color: black;
}

.chart-wrapper {
  height: 350px;
}

.empty-state {
  text-align: center;
  color: grey;
  margin-top: 3rem;
  font-style: italic;
}
</style>
