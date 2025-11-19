<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { store } from '../store.js'

const selectedCity = ref('')
const selectedNeighborhood = ref('')
const selectedPropertyType = ref('')
const priceRange = ref(50)
const rating = ref(0)
const occupancy = ref(1)
const selectedDateRange = ref('')

const selectedFormat = ref('PDF')
const formatNav = ref(null)
const formatGlider = ref(null)

const conversionRates = {
  USD: { symbol: '$', max: 500 },
  EUR: { symbol: '€', max: 470 },
  GBP: { symbol: '£', max: 410 }
}
const currentCurrencyInfo = computed(() => {
  return conversionRates[store.state.currency] || conversionRates.USD
})

const updateFormatGlider = () => {
  if (!formatNav.value || !formatGlider.value) return;
  const activeButton = formatNav.value.querySelector('button.active');
  if (activeButton) {
    formatGlider.value.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    formatGlider.value.style.opacity = '1';
    const offsetLeft = activeButton.offsetLeft;
    const offsetWidth = activeButton.offsetWidth;
    const offsetHeight = activeButton.offsetHeight;

    formatGlider.value.style.width = `${offsetWidth}px`;
    formatGlider.value.style.height = `${offsetHeight}px`;
    formatGlider.value.style.top = `0px`;
    formatGlider.value.style.transform = `translateX(${offsetLeft}px)`;
  } else {
    formatGlider.value.style.opacity = '0';
    formatGlider.value.style.width = '0px';
  }
};

watch(selectedFormat, () => {
  setTimeout(updateFormatGlider, 0);
}, { flush: 'post' });

onMounted(() => {
  updateFormatGlider();
});

function generateReport() {
  console.log('--- Report Generation ---');
  console.log('Filters:', {
    city: selectedCity.value,
    neighborhood: selectedNeighborhood.value,
    propertyType: selectedPropertyType.value,
    priceMax: priceRange.value,
    ratingMin: rating.value,
    occupancyMin: occupancy.value,
    dateRange: selectedDateRange.value,
    currency: store.state.currency,
  });
  console.log('Format:', selectedFormat.value);
  
  alert(`Generating ${selectedFormat.value} report... (Check console for options)`);
}
</script>

<template>
  <div class="export-page">
    <div class="header">
      <h1>Export Data</h1>
    </div>

    <section class="filter-box">
      <div class="filter-row">
        <div class="filter-group">
          <label for="city">City</label>
          <div class="select-box" @click="">
            <span>{{ selectedCity || 'Select City' }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
          </div>
          </div>
        <div class="filter-group">
          <label for="neighborhood">Neighborhood</label>
          <div class="select-box" @click="">
            <span>{{ selectedNeighborhood || 'Select Neighborhood' }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
          </div>
          </div>
        <div class="filter-group">
          <label for="propertyType">Property Type</label>
          <div class="select-box" @click="">
            <span>{{ selectedPropertyType || 'Select Type' }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
          </div>
          </div>
      </div>

      <div class="filter-row sliders">
        
        <div class="filter-group slider-group">
           <div class="slider-header">
             <label for="priceRange">Price Range</label>
             <input type="number" class="slider-input" v-model.number="priceRange" min="50" :max="currentCurrencyInfo.max" step="10">
           </div>
           <div class="slider-wrapper">
             <input type="range" id="priceRange" v-model.number="priceRange" min="50" :max="currentCurrencyInfo.max" step="10">
           </div>
           <div class="slider-limits">
             <span>{{ currentCurrencyInfo.symbol }}50</span>
             <span>{{ currentCurrencyInfo.symbol }}{{ currentCurrencyInfo.max }}</span>
           </div>
         </div>

         <div class="filter-group slider-group">
           <div class="slider-header">
             <label for="rating">Rating</label>
             <input type="text" class="slider-input" v-model.number="rating" min="0" max="5" step="0.1">
           </div>
           <div class="slider-wrapper">
             <input type="range" id="rating" v-model.number="rating" min="0" max="5" step="0.1">
           </div>
           <div class="slider-limits">
             <span>0</span>
             <span>5</span>
           </div>
         </div>

         <div class="filter-group slider-group">
           <div class="slider-header">
             <label for="occupancy">Occupancy</label>
             <input type="number" class="slider-input" v-model.number="occupancy" min="1" max="10" step="1">
           </div>
           <div class="slider-wrapper">
             <input type="range" id="occupancy" v-model.number="occupancy" min="1" max="10" step="1">
           </div>
           <div class="slider-limits">
             <span>1</span>
             <span>10</span>
           </div>
         </div>

      </div>

      <div class="filter-row date-range">
        <button
          :class="{ active: selectedDateRange === 'Last 7 days' }"
          @click="selectedDateRange = 'Last 7 days'">
          Last 7 days
        </button>
        <button
          :class="{ active: selectedDateRange === 'Last month' }"
          @click="selectedDateRange = 'Last month'">
          Last month
        </button>
        <button
          :class="{ active: selectedDateRange === 'Custom' }"
          @click="selectedDateRange = 'Custom'">
          Custom
        </button>
      </div>
    </section>

    <section class="format-box">
      <h3>Choose Format</h3>
      <div class="format-nav" ref="formatNav">
        <button :class="{ active: selectedFormat === 'PDF' }" @click="selectedFormat = 'PDF'">PDF</button>
        <button :class="{ active: selectedFormat === 'CSV' }" @click="selectedFormat = 'CSV'">CSV</button>
        <button :class="{ active: selectedFormat === 'JSON' }" @click="selectedFormat = 'JSON'">JSON</button>
      </div>
    </section>

    <div class="generate-section">
      <button class="btn-generate" @click="generateReport">Generate Report</button>
      <p class="footer-note">Your report will be generated using the filters you've applied.</p>
    </div>

  </div>
</template>

<style scoped>
.export-page {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 820px;
  color: black;
}

.header {
  width: 100%;
}

.header h1 {
  font-weight: 800;
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  color: black;
}

.header .subtitle {
  font-size: 1rem;
  color: dimgrey;
  margin-top: -1rem;
}

.filter-box {
  background-color: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px -5px rgba(150, 150, 150, 0.08);
  display: flex;
  flex-direction: column;
}

.filter-row {
  display: flex;
  gap: 1.5rem;
}

.filter-row.sliders {
  margin-top: 1rem;
}

.filter-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: black;
}

.select-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0rem 1rem;
  border: 1px solid lightgrey;
  border-radius: 8px;
  background-color: white;
  font-size: 0.9rem;
  color: black;
  cursor: pointer;
  user-select: none;
  min-height: 42px;
}

.select-box span {
  opacity: 0.7;
}

.select-box svg {
  color: dimgrey;
}

.sliders {
   gap: 1.5rem; 
}

.slider-group { 
  gap: 0.25rem;
}

.slider-group label {
  font-size: 1rem;
  font-weight: normal;
  color: dimgrey;
}

.slider-wrapper {
  display: flex;
  align-items: center;
}

.slider-wrapper span { 
  font-size: 0.8rem; 
  color: dimgrey; 
  white-space: nowrap;
}

.slider-group input[type="range"] {
  flex-grow: 1;
  width: 100%;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  height: 16px;
}
.slider-group input[type="range"]:focus {
  outline: none;
}

.slider-input {
  width: auto;
  padding: 0;
  border: none;
  border-radius: 0;
  text-align: right;
  font-size: 1.1rem;
  font-weight: normal;
  color: black;
  margin-top: 0;
  background-color: transparent;
}
.slider-input:focus {
  outline: none;
}

.slider-input::-webkit-outer-spin-button,
.slider-input::-webkit-inner-spin-button { margin: 0; -webkit-appearance: none; }
.slider-input[type=number] { appearance: textfield; -moz-appearance: textfield; }

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0.1rem;
}

.slider-limits {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0.1rem;
}

.slider-limits span {
  font-size: 0.85rem;
  color: dimgrey;
}

.slider-group input[type="range"]::-webkit-slider-runnable-track {
  width: 100%;
  height: 4px;
  background-color: lightgrey;
  border-radius: 4px;
}

.slider-group input[type="range"]::-moz-range-track {
  width: 100%;
  height: 4px;
  background-color: lightgrey;
  border-radius: 4px;
}
.slider-group input[type="range"]::-moz-focus-outer {
  border: 0;
}

/* COR ALTERADA */
.slider-group input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  margin-top: -6px;
  background-color: #FF5A5F;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  border: none;
  transition: transform 0.1s ease;
}
.slider-group input[type="range"]:active::-webkit-slider-thumb {
  transform: scale(1.15);
}

/* COR ALTERADA */
.slider-group input[type="range"]::-moz-range-thumb {
  background-color: #FF5A5F;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  border: none;
  transition: transform 0.1s ease;
}
.slider-group input[type="range"]:active::-moz-range-thumb {
  transform: scale(1.15);
}

.filter-row.date-range {
  margin-top: 1rem;
  gap: 0.75rem;
}

.date-range button {
  padding: 0.6rem 1rem;
  border: 1px solid lightgrey;
  background-color: white;
  color: dimgrey;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
/* COR ALTERADA */
.date-range button.active {
  background-color: rgba(255, 90, 95, 0.1);
  color: #FF5A5F;
  border-color: #FF5A5F;
}

.date-range button:not(.active):hover {
  background-color: #f9fafb;
  color: black;
  border-color: black;
}

.format-box {
  align-items: flex-start;
  background-color: white;
  border-radius: 16px;
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
  box-sizing: border-box;
}

.format-box h3 {
  font-size: 1rem;
  font-weight: 600;
  color: black;
  margin: 0;
  width: 100%;
  text-align: left;
}

.format-nav {
  display: flex;
  gap: 0.75rem;
  margin-left: 0;
  margin-right: auto;
  position: relative;
}

.format-glider {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%; 
  /* COR ALTERADA */
  background-color: rgba(255, 90, 95, 0.1);
  border: 1px solid #FF5A5F;
  border-radius: 9999px;
  box-sizing: border-box;
  z-index: 1;
  opacity: 0;
}

.format-nav button {
  background-color: white;
  border: 1px solid lightgrey;
  color: dimgrey;
  padding: 0.6rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 9999px;
  transition: all 0.2s ease;
  text-align: center;
  position: relative;
  z-index: 2;
}

/* COR ALTERADA */
.format-nav button.active {
  background-color: rgba(255, 90, 95, 0.1);
  color: #FF5A5F;
  border-color: #FF5A5F;
}

.format-nav button:not(.active):hover {
  background-color: #f9fafb;
  color: black;
  border-color: black;
}

.generate-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0rem;
}
/* COR ALTERADA */
.btn-generate {
  background-color: #FF5A5F;
  color: white;
  border: none;
  padding: 0.9rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 9999px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  box-shadow: 0 4px 6px rgba(237, 106, 106, 0.2);
}

.btn-generate:hover {
  background-color: #e0484d;
}

.footer-note {
  font-size: 0.8rem;
  color: dimgrey;
  text-align: center;
}
</style>