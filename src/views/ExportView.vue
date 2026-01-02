<template>
  <div class="export-page">
    <div class="header-section">
      <h1>Export Data</h1>
    </div>

    <section class="filter-card">
      <div class="filter-row dropdowns-row">
        <div class="filter-group">
          <label>City</label>
          <div class="select-wrapper">
            <select v-model="selectedCity" @change="onCityChange">
              <option value="porto">Porto</option>
              <option value="lisbon">Lisbon</option>
              <option value="barcelona">Barcelona</option>
            </select>
          </div>
        </div>

        <div class="filter-group">
          <label>Period</label>
          <div class="select-wrapper">
            <select v-model="selectedPeriod" @change="onPeriodChange">
              <option
                v-for="p in store.PERIODS"
                :key="p.value"
                :value="p.value"
              >
                {{ p.label }}
              </option>
            </select>
          </div>
        </div>

        <div class="filter-group">
          <label>Neighbourhood</label>
          <div class="select-wrapper">
            <select
              v-model="filters.neighbourhood"
              :disabled="!neighbourhoods.length"
            >
              <option value="">All Neighbourhoods</option>
              <option v-for="n in neighbourhoods" :key="n" :value="n">
                {{ n }}
              </option>
            </select>
          </div>
        </div>

        <div class="filter-group">
          <label>Property Type</label>
          <div class="select-wrapper">
            <select
              v-model="filters.propertyType"
              :disabled="!propertyTypes.length"
            >
              <option value="">All Types</option>
              <option v-for="t in propertyTypes" :key="t" :value="t">
                {{ t }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="filter-row full-width-row">
        <div class="slider-group price-slider">
          <div class="slider-header">
            <label>Price Range</label>
          </div>
          <div class="range-container">
            <input
              type="range"
              min="0"
              max="510"
              step="10"
              v-model.number="filters.priceMin"
              class="thumb thumb-left"
              :style="{ zIndex: filters.priceMin > 250 ? '5' : '3' }"
            />
            <input
              type="range"
              min="0"
              max="510"
              step="10"
              v-model.number="filters.priceMax"
              class="thumb thumb-right"
            />
            <div class="slider-track"></div>
          </div>
          <div class="slider-labels">
            <span>{{ currencySymbol }}{{ filters.priceMin }}</span>
            <span
              >{{ currencySymbol
              }}{{ filters.priceMax >= 510 ? "500+" : filters.priceMax }}</span
            >
          </div>
        </div>
      </div>

      <div class="filter-row secondary-sliders-row">
        <div class="slider-group">
          <div class="slider-header">
            <label>Rating</label>
            <span class="slider-value">{{ filters.minRating }}</span>
          </div>
          <div class="range-container single">
            <input
              type="range"
              min="1"
              max="5"
              step="0.5"
              v-model.number="filters.minRating"
              class="simple-slider"
            />
            <div class="slider-track"></div>
          </div>
          <div class="slider-labels">
            <span>1</span>
            <span>5</span>
          </div>
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <label>Occupancy</label>
            <span class="slider-value">{{
              filters.minGuests >= 10 ? "10+" : filters.minGuests
            }}</span>
          </div>
          <div class="range-container single">
            <input
              type="range"
              min="1"
              max="10"
              step="1"
              v-model.number="filters.minGuests"
              class="simple-slider"
            />
            <div class="slider-track"></div>
          </div>
          <div class="slider-labels">
            <span>1</span>
            <span>10+</span>
          </div>
        </div>
      </div>
    </section>

    <section class="action-card">
      <div class="action-header">
        <h3>Ready to Export?</h3>
        <p>
          This will generate a PDF with the
          {{ filteredListings.length }} listings matching your criteria.
        </p>
      </div>
      <button
        class="btn-export"
        @click="exportPDF"
        :disabled="isLoading || filteredListings.length === 0"
      >
        <span v-if="!isLoading">Download PDF Report</span>
        <span v-else>Generating...</span>
      </button>
    </section>

    <section class="preview-card">
      <h3>Preview Data</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Neighbourhood</th>
              <th>Type</th>
              <th>Price</th>
              <th>Guests</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in previewList" :key="item.id">
              <td class="col-name">{{ item.name }}</td>
              <td>{{ item.neighbourhood_cleansed }}</td>
              <td>{{ item.room_type }}</td>
              <td>{{ currencySymbol }}{{ item.price }}</td>
              <td>{{ item.accommodates }}</td>
              <td>{{ item.review_scores_rating || "N/A" }}</td>
            </tr>
            <tr v-if="filteredListings.length === 0">
              <td colspan="6" class="empty-row">
                No data matches your filters.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="pagination-info" v-if="filteredListings.length > 0">
        Showing top 10 of {{ filteredListings.length }} results
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import { store } from "../store.js";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

const selectedCity = ref("porto");
const selectedPeriod = ref(store.state.period);
const rawListings = ref([]);
const isLoading = ref(false);

const onPeriodChange = () => {
  store.savePeriod(selectedPeriod.value);
  loadData();
};

const filters = reactive({
  neighbourhood: "",
  propertyType: "",
  priceMin: 0,
  priceMax: 510,
  minRating: 1,
  minGuests: 1,
});

const currencySymbol = computed(() => {
  const map = { USD: "$", EUR: "€", GBP: "£" };
  return map[store.state.currency] || "€";
});

const conversionRate = computed(() => {
  const rates = { EUR: 1, USD: 1.08, GBP: 0.85 };
  return rates[store.state.currency] || 1;
});

const neighbourhoods = computed(() => {
  const set = new Set(rawListings.value.map((i) => i.neighbourhood_cleansed));
  return Array.from(set).sort();
});

const propertyTypes = computed(() => {
  const set = new Set(rawListings.value.map((i) => i.room_type));
  return Array.from(set).sort();
});

const filteredListings = computed(() => {
  return rawListings.value.filter((item) => {
    const price = parseFloat(String(item.price).replace(/[$,]/g, "")) || 0;

    if (price <= 0) return false;
    if (price < filters.priceMin) return false;
    if (filters.priceMax < 510 && price > filters.priceMax) return false;

    if (
      filters.neighbourhood &&
      item.neighbourhood_cleansed !== filters.neighbourhood
    )
      return false;
    if (filters.propertyType && item.room_type !== filters.propertyType)
      return false;

    const rating = parseFloat(item.review_scores_rating || 0);
    const normRating = rating > 5 ? rating / 20 : rating;
    if (normRating < filters.minRating) return false;

    const capacity = parseInt(item.accommodates) || 1;
    if (filters.minGuests >= 10) {
      if (capacity < 10) return false;
    } else {
      if (capacity < filters.minGuests) return false;
    }

    return true;
  });
});

const previewList = computed(() => filteredListings.value.slice(0, 10));

const loadData = async () => {
  isLoading.value = true;
  let cityKey = selectedCity.value.toLowerCase();
  if (cityKey === "lisboa") cityKey = "lisbon";
  const periodKey = selectedPeriod.value.replace("-", "_");

  try {
    const response = await fetch(
      `http://localhost:3000/${cityKey}_${periodKey}_listings`
    );
    if (!response.ok) throw new Error("Failed to fetch");
    rawListings.value = await response.json();

    filters.neighbourhood = "";
    filters.propertyType = "";
  } catch (err) {
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

const onCityChange = () => {
  loadData();
};

const exportPDF = () => {
  const doc = new jsPDF();
  doc.setFontSize(18);
  doc.text(`InsideView Report - ${selectedCity.value.toUpperCase()}`, 14, 22);

  const activeFilters = [];
  if (filters.neighbourhood)
    activeFilters.push(`Hood: ${filters.neighbourhood}`);
  if (filters.propertyType) activeFilters.push(`Type: ${filters.propertyType}`);

  const minPriceConverted = Math.round(filters.priceMin * conversionRate.value);
  const maxPriceConverted =
    filters.priceMax >= 510
      ? "500+"
      : Math.round(filters.priceMax * conversionRate.value);
  activeFilters.push(
    `Price: ${currencySymbol.value}${minPriceConverted}-${maxPriceConverted}`
  );
  activeFilters.push(`Rating: ${filters.minRating}+`);
  activeFilters.push(`Guests: ${filters.minGuests}+`);

  const filterString = `Generated: ${new Date().toLocaleDateString()} | ${activeFilters.join(
    ", "
  )}`;

  doc.setFontSize(10);
  doc.setTextColor(100);
  const splitTitle = doc.splitTextToSize(filterString, 180);
  doc.text(splitTitle, 14, 30);

  const startY = 32 + splitTitle.length * 5;

  const tableBody = filteredListings.value.slice(0, 1000).map((item) => {
    const price = parseFloat(String(item.price).replace(/[$,]/g, "")) || 0;
    const convertedPrice = Math.round(price * conversionRate.value);
    return [
      item.name,
      item.neighbourhood_cleansed,
      item.room_type,
      price > 0 ? `${currencySymbol.value}${convertedPrice}` : "N/A",
      item.accommodates,
      item.review_scores_rating || "-",
    ];
  });

  autoTable(doc, {
    head: [["Name", "Neighbourhood", "Type", "Price", "Guests", "Rating"]],
    body: tableBody,
    startY: startY,
    theme: "grid",
    styles: {
      fontSize: 8,
      cellPadding: 3,
      overflow: "linebreak",
      valign: "middle",
    },
    headStyles: { fillColor: [255, 90, 95] },
    columnStyles: {
      0: { cellWidth: 60 },
      1: { cellWidth: 35 },
      2: { cellWidth: 30 },
      3: { cellWidth: 25 },
      4: { cellWidth: 15 },
      5: { cellWidth: 15 },
    },
  });

  doc.save(`report_${selectedCity.value}_${Date.now()}.pdf`);
};

onMounted(() => {
  loadData();
});

watch(
  () => filters.priceMin,
  (val) => {
    if (val >= filters.priceMax - 10) {
      filters.priceMin = filters.priceMax - 10;
    }
  }
);

watch(
  () => filters.priceMax,
  (val) => {
    if (val <= filters.priceMin + 10) {
      filters.priceMax = filters.priceMin + 10;
    }
  }
);
</script>

<style scoped>
/* LAYOUT */
.export-page {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
  color: black;
}

/* HEADER */
.header-section {
  margin-bottom: 2rem;
}

.header-section h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 800;
}

/* CARDS */
.filter-card,
.action-card,
.preview-card {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.02);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

/* LAYOUT GRIDS */
.dropdowns-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.full-width-row {
  display: block;
  width: 100%;
  margin-bottom: 2.5rem;
}

.secondary-sliders-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

/* FILTER GROUPS */
.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: grey;
}

.select-wrapper select {
  width: 100%;
  padding: 10px 12px;
  font-size: 0.9rem;
  color: black;
  background: white;
  border: 1px solid lightgrey;
  border-radius: 8px;
  outline: none;
}

/* SLIDER HEADERS */
.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.slider-header label {
  font-size: 0.85rem;
  color: grey;
}

.slider-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: black;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: grey;
}

/* RANGE SLIDER */
.range-container {
  position: relative;
  display: flex;
  align-items: center;
  height: 14px;
  margin-top: 10px;
}

.slider-track {
  position: absolute;
  top: 50%;
  z-index: 0;
  width: 100%;
  height: 6px;
  background-color: #e5e7eb;
  border-radius: 3px;
  transform: translateY(-50%);
}

input[type="range"] {
  position: absolute;
  top: 0;
  z-index: 2;
  width: 100%;
  height: 14px;
  margin: 0;
  background: transparent;
  pointer-events: none;
  -webkit-appearance: none;
}

.range-container.single input[type="range"] {
  pointer-events: auto;
}

input[type="range"]::-webkit-slider-thumb {
  width: 14px;
  height: 14px;
  margin-top: 0;
  background-color: #ff5a5f;
  border: none;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  pointer-events: all;
  transition: transform 0.1s ease;
  -webkit-appearance: none;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

input[type="range"]::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background-color: #ff5a5f;
  border: none;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  cursor: pointer;
}

.thumb-left {
  z-index: 3;
}

.thumb-right {
  z-index: 4;
}

/* ACTION CARD */
.action-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fafafa;
  border: 1px dashed #ddd;
}

.action-header h3 {
  margin: 0 0 0.2rem 0;
  font-size: 1.1rem;
}

.action-header p {
  margin: 0;
  font-size: 0.9rem;
  color: grey;
}

.btn-export {
  padding: 12px 24px;
  font-weight: 600;
  color: white;
  background-color: #ff5a5f;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-export:disabled {
  background-color: #ffaeb1;
  cursor: not-allowed;
}

.btn-export:hover:not(:disabled) {
  background-color: #e0484d;
}

/* PREVIEW CARD */
.preview-card h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  font-size: 0.9rem;
  border-collapse: collapse;
}

th {
  padding: 12px;
  font-size: 0.75rem;
  color: grey;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #f0f0f0;
}

td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.col-name {
  font-weight: 600;
  color: #333;
}

.empty-row {
  padding: 2rem;
  color: grey;
  font-style: italic;
  text-align: center;
}

.pagination-info {
  margin-top: 1rem;
  font-size: 0.8rem;
  color: grey;
  text-align: right;
}
</style>
