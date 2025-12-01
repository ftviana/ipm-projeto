<template>
  <div class="export-page">
    <div class="header-section">
      <h1>Export Data</h1>
      <p class="subtitle">
        Generate and download a report based on your selected filters.
      </p>
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

// --- STATE ---
const selectedCity = ref("porto");
const rawListings = ref([]);
const isLoading = ref(false);

const filters = reactive({
  neighbourhood: "",
  propertyType: "",
  priceMin: 0,
  priceMax: 510, // MUDANÇA: Default max é 510 (que representa 500+)
  minRating: 1,
  minGuests: 1,
});

// --- COMPUTED ---
const currencySymbol = computed(() => {
  const map = { USD: "$", EUR: "€", GBP: "£" };
  return map[store.state.currency] || "€";
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
    // Price Logic Atualizada
    const price = parseFloat(String(item.price).replace(/[$,]/g, "")) || 0;

    if (price <= 0) return false; // Ignorar preços zero
    if (price < filters.priceMin) return false;

    // Lógica 500+: Se priceMax < 510, aplicamos o limite.
    // Se for 510, ignoramos o limite superior (mostra tudo > priceMin)
    if (filters.priceMax < 510 && price > filters.priceMax) return false;

    // Neighbourhood
    if (
      filters.neighbourhood &&
      item.neighbourhood_cleansed !== filters.neighbourhood
    )
      return false;

    // Property Type
    if (filters.propertyType && item.room_type !== filters.propertyType)
      return false;

    // Rating
    const rating = parseFloat(item.review_scores_rating || 0);
    const normRating = rating > 5 ? rating / 20 : rating;
    if (normRating < filters.minRating) return false;

    // Capacity
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

// --- ACTIONS ---
const loadData = async () => {
  isLoading.value = true;
  let cityKey = selectedCity.value.toLowerCase();
  if (cityKey === "lisboa") cityKey = "lisbon";

  try {
    const response = await fetch(`http://localhost:3000/${cityKey}_listings`);
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

// --- PDF EXPORT ---
const exportPDF = () => {
  const doc = new jsPDF();
  doc.setFontSize(18);
  doc.text(`InsideView Report - ${selectedCity.value.toUpperCase()}`, 14, 22);

  const activeFilters = [];
  if (filters.neighbourhood)
    activeFilters.push(`Hood: ${filters.neighbourhood}`);
  if (filters.propertyType) activeFilters.push(`Type: ${filters.propertyType}`);

  // Display 500+ correct text
  const maxPrice = filters.priceMax >= 510 ? "500+" : filters.priceMax;
  activeFilters.push(
    `Price: ${currencySymbol.value}${filters.priceMin}-${maxPrice}`
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
    return [
      item.name,
      item.neighbourhood_cleansed,
      item.room_type,
      price > 0 ? `${currencySymbol.value}${price}` : "N/A",
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

// --- INIT ---
onMounted(() => {
  loadData();
});

// --- WATCHERS DE BLOQUEIO (GAP) ---
watch(
  () => filters.priceMin,
  (val) => {
    // Se o mínimo tentar passar o máximo (menos o gap de 10), empurra-o para trás
    if (val >= filters.priceMax - 10) {
      filters.priceMin = filters.priceMax - 10;
    }
  }
);

watch(
  () => filters.priceMax,
  (val) => {
    // Se o máximo tentar baixar do mínimo (mais o gap de 10), empurra-o para a frente
    if (val <= filters.priceMin + 10) {
      filters.priceMax = filters.priceMin + 10;
    }
  }
);
</script>

<style scoped>
.export-page {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 900px;
  margin: 0 auto;
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

.subtitle {
  color: grey;
  margin: 0;
}

/* CARDS */
.filter-card,
.action-card,
.preview-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.02);
  margin-bottom: 2rem;
}

/* LAYOUT GRIDS */
.dropdowns-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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
  font-size: 0.85rem;
  font-weight: 600;
  color: grey;
  margin-bottom: 0.5rem;
}

.select-wrapper select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid lightgrey;
  border-radius: 8px;
  font-size: 0.9rem;
  color: black;
  background: white;
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

/* --- SLIDER CSS --- */
.range-container {
  position: relative;
  height: 14px;
  margin-top: 10px;
  display: flex;
  align-items: center;
}

.slider-track {
  position: absolute;
  width: 100%;
  height: 6px;
  background-color: #e5e7eb;
  border-radius: 3px;
  z-index: 0;
  top: 50%;
  transform: translateY(-50%);
}

/* Range Inputs */
input[type="range"] {
  -webkit-appearance: none;
  pointer-events: none;
  position: absolute;
  width: 100%;
  height: 14px;
  background: transparent;
  z-index: 2;
  margin: 0;
  top: 0;
}

.range-container.single input[type="range"] {
  pointer-events: auto;
}

/* THUMBS (BALLS) */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  pointer-events: all;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background-color: #ff5a5f;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  transition: transform 0.1s ease;
  margin-top: 0;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

input[type="range"]::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background-color: #ff5a5f;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* Z-Index for Dual Sliders */
.thumb-left {
  z-index: 3;
}
.thumb-right {
  z-index: 4;
}

/* OTHER STYLES */
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
  background-color: #ff5a5f;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
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

.preview-card h3 {
  margin-top: 0;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

th {
  text-align: left;
  padding: 12px;
  border-bottom: 2px solid #f0f0f0;
  color: grey;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  text-align: center;
  color: grey;
  padding: 2rem;
  font-style: italic;
}

.pagination-info {
  margin-top: 1rem;
  font-size: 0.8rem;
  color: grey;
  text-align: right;
}
</style>
