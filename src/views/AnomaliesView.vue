<template>
  <div class="anomalies-page">
    <div class="header-section">
      <div class="header-left">
        <h1>Anomalies & Alerts</h1>
      </div>
    </div>

    <div class="filters-bar">
      <div class="input-group">
        <svg
          class="search-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
        >
          <path
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <select v-model="selectedCity" @change="loadData">
          <option value="porto">Porto</option>
          <option value="lisbon">Lisbon</option>
          <option value="barcelona">Barcelona</option>
        </select>
      </div>

      <div class="input-group">
        <svg
          class="search-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
        >
          <path
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3 12h18M3 6h18M3 18h18"
          />
        </svg>
        <select
          v-model="selectedNeighborhood"
          :disabled="!neighborhoods.length"
        >
          <option value="">All Neighborhoods</option>
          <option v-for="n in neighborhoods" :key="n" :value="n">
            {{ n }}
          </option>
        </select>
      </div>

      <button class="btn-apply" @click="resetFilters">Reset</button>
    </div>

    <div class="alerts-grid">
      <div class="alert-card">
        <div class="card-header-row">
          <div class="icon-wrapper red-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"
              />
            </svg>
          </div>
          <h3>Hosts with >10 properties</h3>
        </div>
        <p class="card-description">
          Hosts managing an unusually high number of listings.
        </p>
        <button class="btn-view" @click="activeAnomaly = 'multiHost'">
          View Details
        </button>
      </div>

      <div class="alert-card">
        <div class="card-header-row">
          <div class="icon-wrapper red-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"
              />
            </svg>
          </div>
          <h3>>300 occupied days</h3>
        </div>
        <p class="card-description">
          Listings with near-permanent occupancy rates.
        </p>
        <button class="btn-view" @click="activeAnomaly = 'highOccupancy'">
          View Details
        </button>
      </div>

      <div class="alert-card">
        <div class="card-header-row">
          <div class="icon-wrapper red-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"
              />
            </svg>
          </div>
          <h3>Low rating (&lt; 3★)</h3>
        </div>
        <p class="card-description">
          Consistently poor guest ratings by houses and guests.
        </p>
        <button class="btn-view" @click="activeAnomaly = 'lowRating'">
          View Details
        </button>
      </div>

      <div class="alert-card">
        <div class="card-header-row">
          <div class="icon-wrapper red-icon">
            <svg
              style="transform: scaleY(-1)"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"
              />
            </svg>
          </div>
          <h3>Low occupancy (&lt; 60%)</h3>
        </div>
        <p class="card-description">
          Listings with unusually low booking rates.
        </p>
        <button class="btn-view" @click="activeAnomaly = 'lowOccupancy'">
          View Details
        </button>
      </div>

      <div class="alert-card">
        <div class="card-header-row">
          <div class="icon-wrapper red-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"
              />
            </svg>
          </div>
          <h3>Price Variations (> 4x Avg)</h3>
        </div>
        <p class="card-description">
          Significant and suspicious price fluctuations.
        </p>
        <button class="btn-view" @click="activeAnomaly = 'priceSpike'">
          View Details
        </button>
      </div>

      <div class="alert-card">
        <div class="card-header-row">
          <div class="icon-wrapper red-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"
              />
            </svg>
          </div>
          <h3>Zero / Null Price</h3>
        </div>
        <p class="card-description">
          Data integrity issues or listings with invalid pricing.
        </p>
        <button class="btn-view" @click="activeAnomaly = 'zeroPrice'">
          View Details
        </button>
      </div>
    </div>

    <div class="details-section">
      <h2>
        Detailed Listings: <span>{{ anomalyTitle }}</span>
      </h2>

      <div class="table-card">
        <div v-if="isLoading" class="loading-state">Scanning data...</div>

        <table v-else>
          <thead>
            <tr>
              <th>ANOMALY CATEGORY</th>
              <th>LISTINGS COUNT</th>
              <th>AFFECTED HOSTS</th>
              <th>AVG. SEVERITY</th>
              <th>EXPORT</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in currentTableData" :key="item.id">
              <td>
                <span class="tag-anomaly">{{ item.category }}</span>
              </td>

              <td class="fw-bold">
                {{ activeAnomaly === "multiHost" ? item.metric : item.name }}
              </td>

              <td>
                {{ activeAnomaly === "multiHost" ? item.name : item.sub }}
              </td>

              <td>
                <span class="metric-value">{{
                  activeAnomaly === "multiHost" ? item.metric : item.metric
                }}</span>
              </td>

              <td><button class="btn-table">Inspect</button></td>
            </tr>

            <tr v-if="currentTableData.length === 0">
              <td colspan="5" class="empty-row">
                No anomalies found for this category.
              </td>
            </tr>
          </tbody>
        </table>

        <div class="table-footer-bar"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, shallowRef } from "vue";
import { store } from "../store.js";

// --- STATE ---
const selectedCity = ref("porto");
const selectedNeighborhood = ref("");
const rawListings = shallowRef([]);
const isLoading = ref(false);
const activeAnomaly = ref("multiHost");

// --- COMPUTED HELPERS ---
const currencySymbol = computed(() => {
  const map = { USD: "$", EUR: "€", GBP: "£" };
  return map[store.state.currency] || "€";
});

const neighborhoods = computed(() => {
  if (!rawListings.value.length) return [];
  const set = new Set(rawListings.value.map((i) => i.neighbourhood_cleansed));
  return Array.from(set).sort();
});

const formatPrice = (val) => {
  const num = parseFloat(String(val).replace(/[$,]/g, "")) || 0;
  return `${currencySymbol.value}${num}`;
};

// --- DATA LOADING ---
const loadData = async () => {
  isLoading.value = true;
  let cityKey = selectedCity.value.toLowerCase();
  if (cityKey === "lisboa") cityKey = "lisbon";

  try {
    const response = await fetch(`http://localhost:3000/${cityKey}_listings`);
    if (!response.ok) throw new Error("Failed");
    const data = await response.json();
    rawListings.value = Object.freeze(data);
  } catch (e) {
    console.error(e);
  } finally {
    isLoading.value = false;
  }
};

const resetFilters = () => {
  selectedNeighborhood.value = "";
};

// --- ANOMALY LOGIC ---

// 1. Multi-Host Data
const multiHostData = computed(() => {
  const hosts = {};
  rawListings.value.forEach((item) => {
    if (
      selectedNeighborhood.value &&
      item.neighbourhood_cleansed !== selectedNeighborhood.value
    )
      return;

    const hid = item.host_id;
    if (!hid) return;
    if (!hosts[hid]) hosts[hid] = { id: hid, name: item.host_name, count: 0 };
    hosts[hid].count++;
  });

  return Object.values(hosts)
    .filter((h) => h.count > 10)
    .sort((a, b) => b.count - a.count)
    .slice(0, 50)
    .map((h) => ({
      id: h.id,
      name: h.name,
      sub: `ID: ${h.id}`,
      category: "Commercial Host",
      metric: `${h.count} Listings`,
      price: "-",
    }));
});

// 2. High Occupancy (>300 days)
const highOccupancyData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        selectedNeighborhood.value &&
        i.neighbourhood_cleansed !== selectedNeighborhood.value
      )
        return false;
      const occupied = 365 - (parseInt(i.availability_365) || 0);
      return occupied > 300;
    })
    .slice(0, 50)
    .map((i) => ({
      id: i.id,
      name: i.name,
      sub: i.neighbourhood_cleansed,
      category: "High Occupancy",
      metric: `${365 - (parseInt(i.availability_365) || 0)} days`,
      price: formatPrice(i.price),
    }));
});

// 3. Low Rating (< 3 Stars)
const lowRatingData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        selectedNeighborhood.value &&
        i.neighbourhood_cleansed !== selectedNeighborhood.value
      )
        return false;
      if (!i.review_scores_rating) return false;
      let r = parseFloat(i.review_scores_rating);
      if (r > 5) r = r / 20;
      return r < 3 && r > 0;
    })
    .slice(0, 50)
    .map((i) => ({
      id: i.id,
      name: i.name,
      sub: i.neighbourhood_cleansed,
      category: "Poor Quality",
      metric: `${i.review_scores_rating} ★`,
      price: formatPrice(i.price),
    }));
});

// 4. Low Occupancy (< 60 days)
const lowOccupancyData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        selectedNeighborhood.value &&
        i.neighbourhood_cleansed !== selectedNeighborhood.value
      )
        return false;
      const occupied = 365 - (parseInt(i.availability_365) || 0);
      return occupied < 60;
    })
    .slice(0, 50)
    .map((i) => ({
      id: i.id,
      name: i.name,
      sub: i.neighbourhood_cleansed,
      category: "Low Demand",
      metric: `${365 - (parseInt(i.availability_365) || 0)} days occupied`,
      price: formatPrice(i.price),
    }));
});

// 5. Price Outliers (> 4x Avg)
const priceOutlierData = computed(() => {
  if (!rawListings.value.length) return [];
  let total = 0,
    count = 0;
  rawListings.value.forEach((i) => {
    total += parseFloat(String(i.price).replace(/[$,]/g, "")) || 0;
    count++;
  });
  const avg = total / count;

  return rawListings.value
    .filter((i) => {
      if (
        selectedNeighborhood.value &&
        i.neighbourhood_cleansed !== selectedNeighborhood.value
      )
        return false;
      const p = parseFloat(String(i.price).replace(/[$,]/g, "")) || 0;
      return p > avg * 4;
    })
    .sort(
      (a, b) =>
        parseFloat(String(b.price).replace(/[$,]/g, "")) -
        parseFloat(String(a.price).replace(/[$,]/g, ""))
    )
    .slice(0, 50)
    .map((i) => ({
      id: i.id,
      name: i.name,
      sub: i.neighbourhood_cleansed,
      category: "Price Spike",
      metric: "+400% vs Avg",
      price: formatPrice(i.price),
    }));
});

// 6. Zero Price
const zeroPriceData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        selectedNeighborhood.value &&
        i.neighbourhood_cleansed !== selectedNeighborhood.value
      )
        return false;
      const p = parseFloat(String(i.price).replace(/[$,]/g, "")) || 0;
      return p === 0;
    })
    .slice(0, 50)
    .map((i) => ({
      id: i.id,
      name: i.name || "Unknown Listing",
      sub: i.neighbourhood_cleansed,
      category: "Data Error",
      metric: "Invalid Price",
      price: "€0",
    }));
});

const currentTableData = computed(() => {
  switch (activeAnomaly.value) {
    case "multiHost":
      return multiHostData.value;
    case "highOccupancy":
      return highOccupancyData.value;
    case "lowRating":
      return lowRatingData.value;
    case "lowOccupancy":
      return lowOccupancyData.value;
    case "priceSpike":
      return priceOutlierData.value;
    case "zeroPrice":
      return zeroPriceData.value;
    default:
      return [];
  }
});

const anomalyTitle = computed(() => {
  switch (activeAnomaly.value) {
    case "multiHost":
      return "Hosts with >10 Properties";
    case "highOccupancy":
      return "High Occupancy Listings";
    case "lowRating":
      return "Low Rated Listings";
    case "lowOccupancy":
      return "Low Demand Listings";
    case "priceSpike":
      return "Price Outliers";
    case "zeroPrice":
      return "Zero Price Listings";
    default:
      return "";
  }
});

onMounted(loadData);
</script>

<style scoped>
.anomalies-page {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 1000px;
  color: black;
}

.header-section {
  margin-bottom: 2rem;
}
.header-section h1 {
  font-weight: 800;
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
}

/* FILTERS BAR */
.filters-bar {
  display: flex;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  align-items: center;
}

.input-group {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: grey;
  pointer-events: none;
}

.filters-bar select {
  width: 100%;
  padding: 10px 12px 10px 40px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9rem;
  color: black;
  background: #f9fafb;
  outline: none;
  cursor: pointer;
}

.btn-apply {
  background-color: #ff5a5f;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

/* ALERTS GRID */
.alerts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.alert-card {
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 200px;
}

.card-header-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.icon-wrapper {
  color: #ff5a5f;
  display: flex;
}
.icon-wrapper svg {
  width: 24px;
  height: 24px;
}

.alert-card h3 {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0;
  color: #333;
  line-height: 1.3;
}

.card-description {
  font-size: 0.85rem;
  color: grey;
  line-height: 1.5;
  margin: 0 0 1.5rem 0;
  flex-grow: 1;
}

.btn-view {
  width: 100%;
  background-color: #fff0f0;
  color: #ff5a5f;
  border: none;
  padding: 10px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-view:hover {
  background-color: #ffe0e0;
}

/* DETAILS SECTION & TABLE */
.details-section h2 {
  font-size: 1.4rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  color: #333;
}

.details-section h2 span {
  color: #ff5a5f;
}

.table-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

th {
  text-align: left;
  padding: 16px 24px;
  background-color: #f9fafb;
  color: #6b7280;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

td {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
  color: #333;
}

.name-cell {
  display: flex;
  flex-direction: column;
}
.sub-text {
  font-size: 0.8rem;
  color: grey;
}
.fw-bold {
  font-weight: 700;
}

.tag-anomaly {
  background: #fff0f0;
  color: #ff5a5f;
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.metric-value {
  font-weight: 600;
  color: #333;
}

.btn-table {
  border: 1px solid #e5e7eb;
  background: white;
  color: #333;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 600;
  transition: all 0.2s;
}
.btn-table:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.table-footer-bar {
  height: 20px;
  background: white;
}

.empty-row,
.loading-state {
  text-align: center;
  padding: 3rem;
  color: grey;
  font-style: italic;
}
</style>
