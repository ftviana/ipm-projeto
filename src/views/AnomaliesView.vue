<!-- 
  Vista Anomalies - Deteção e análise de anomalias nos dados.
  
  Tipos de anomalias detetadas:
  - Multi-hosts: hosts com mais de 10 propriedades
  - High Occupancy: listings com mais de 300 dias ocupados
  - Low Rating: listings com avaliação inferior a 3 estrelas
  - Low Occupancy: listings com menos de 60 dias ocupados
  - Price Spikes: preços 4x acima da média
  - Zero Price: listings com preço zero ou inválido
  
  Funcionalidades: filtros por cidade/período/bairro, tabela paginada, exportação PDF por linha.
-->
<template>
  <div class="anomalies-page">
    <div class="header-section">
      <div class="header-left">
        <h1>Anomalies</h1>
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
        <select v-model="selectedCity">
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
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
        <select v-model="selectedPeriod">
          <option v-for="p in store.PERIODS" :key="p.value" :value="p.value">
            {{ p.label }}
          </option>
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
          v-model="selectedneighbourhood"
          :disabled="!neighbourhoods.length"
        >
          <option value="">All Neighbourhoods</option>
          <option v-for="n in neighbourhoods" :key="n" :value="n">
            {{ n }}
          </option>
        </select>
      </div>

      <button class="btn-apply" @click="applyFilters">Apply</button>
      <button class="btn-reset" @click="resetFilters">Reset</button>
    </div>

    <div v-if="hasApplied" class="alerts-grid">
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

    <div v-if="hasApplied" class="details-section">
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
              <th>EXPORT</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in paginatedTableData" :key="item.id">
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
                <button class="btn-export-csv" @click="exportAnomalyRow(item)">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                  Export PDF
                </button>
              </td>
            </tr>

            <tr v-if="paginatedTableData.length === 0">
              <td colspan="4" class="empty-row">
                No anomalies found for this category.
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="totalPages > 1" class="pagination">
          <button
            class="pagination-btn"
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
          >
            ← Previous
          </button>
          <span class="pagination-info">
            Page {{ currentPage }} of {{ totalPages }} ({{
              currentTableData.length
            }}
            items)
          </span>
          <button
            class="pagination-btn"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            Next →
          </button>
        </div>

        <div class="table-footer-bar"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, shallowRef, watch, onMounted } from "vue";
import { store } from "../store.js";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

// Estado dos filtros (antes e depois de aplicar)
const selectedCity = ref("porto");
const selectedPeriod = ref("2025-09");
const selectedneighbourhood = ref("");
const appliedCity = ref("porto");
const appliedPeriod = ref("2025-09");
const appliedneighbourhood = ref("");

// Dados e estado da UI
const rawListings = shallowRef([]);
const previewListings = shallowRef([]); // Para popular o dropdown de bairros
const isLoading = ref(false);
const activeAnomaly = ref("multiHost"); // Categoria de anomalia selecionada
const hasApplied = ref(false); // Se os filtros já foram aplicados
const currentPage = ref(1);
const itemsPerPage = 10;

/*
  Carrega os bairros disponíveis para o dropdown antes de aplicar filtros.
*/
const loadNeighbourhoods = async () => {
  let cityKey = selectedCity.value.toLowerCase();
  if (cityKey === "lisboa") cityKey = "lisbon";
  const periodKey = selectedPeriod.value.replace("-", "_");
  try {
    const response = await fetch(
      `http://localhost:3000/${cityKey}_${periodKey}_listings`
    );
    if (!response.ok) throw new Error("Failed");
    const data = await response.json();
    previewListings.value = Object.freeze(data);
  } catch (e) {
    console.error(e);
  }
};

/*
  Aplica os filtros selecionados e carrega os dados para análise de anomalias.
*/
const applyFilters = () => {
  appliedCity.value = selectedCity.value;
  appliedPeriod.value = selectedPeriod.value;
  appliedneighbourhood.value = selectedneighbourhood.value;
  store.savePeriod(selectedPeriod.value);
  hasApplied.value = true;
  loadData();
};

const currencySymbol = computed(() => {
  const map = { USD: "$", EUR: "€", GBP: "£" };
  return map[store.state.currency] || "€";
});

const conversionRate = computed(() => {
  const rates = { EUR: 1, USD: 1.08, GBP: 0.85 };
  return rates[store.state.currency] || 1;
});

const neighbourhoods = computed(() => {
  if (!previewListings.value.length) return [];
  const set = new Set(
    previewListings.value.map((i) => i.neighbourhood_cleansed)
  );
  return Array.from(set).sort();
});

/*
  Formata um valor de preço para a moeda selecionada.
*/
const formatPrice = (val) => {
  const num = parseFloat(String(val).replace(/[$,]/g, "")) || 0;
  const converted = Math.round(num * conversionRate.value);
  return `${currencySymbol.value}${converted}`;
};

/*
  Carrega os dados da API para os filtros aplicados.
*/
const loadData = async () => {
  isLoading.value = true;
  let cityKey = appliedCity.value.toLowerCase();
  if (cityKey === "lisboa") cityKey = "lisbon";
  const periodKey = appliedPeriod.value.replace("-", "_");

  try {
    const response = await fetch(
      `http://localhost:3000/${cityKey}_${periodKey}_listings`
    );
    if (!response.ok) throw new Error("Failed");
    const data = await response.json();
    rawListings.value = Object.freeze(data);
  } catch (e) {
    console.error(e);
  } finally {
    isLoading.value = false;
  }
};

/*
  Reinicia todos os filtros para os valores por defeito.
*/
const resetFilters = () => {
  selectedCity.value = "porto";
  selectedPeriod.value = "2025-09";
  selectedneighbourhood.value = "";
  appliedCity.value = "porto";
  appliedPeriod.value = "2025-09";
  appliedneighbourhood.value = "";
  hasApplied.value = false;
  store.savePeriod("2025-09");
  loadNeighbourhoods();
};

watch([selectedCity, selectedPeriod], () => {
  selectedneighbourhood.value = "";
  loadNeighbourhoods();
});

onMounted(loadNeighbourhoods);

/*
  Computed que identifica hosts com mais de 10 propriedades (hosts comerciais).
  Agrupa listings por host_id e filtra os que excedem o limite.
*/
const multiHostData = computed(() => {
  const hosts = {};
  rawListings.value.forEach((item) => {
    if (
      appliedneighbourhood.value &&
      item.neighbourhood_cleansed !== appliedneighbourhood.value
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
    .map((h) => ({
      id: h.id,
      name: h.name,
      sub: `ID: ${h.id}`,
      category: "Commercial Host",
      metric: `${h.count} Listings`,
      price: "-",
    }));
});

/*
  Computed que identifica listings com mais de 300 dias ocupados por ano.
  Indica possível uso não-turístico ou dados incorretos.
*/
const highOccupancyData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        appliedneighbourhood.value &&
        i.neighbourhood_cleansed !== appliedneighbourhood.value
      )
        return false;
      const avail = parseInt(i.availability_365);
      if (isNaN(avail)) return false;
      const occupied = 365 - avail;
      return occupied > 300;
    })
    .map((i) => {
      const occupied = 365 - parseInt(i.availability_365);
      return {
        id: i.id,
        name: i.name,
        sub: i.neighbourhood_cleansed,
        category: "High Occupancy",
        metric: `${occupied} days`,
        price: formatPrice(i.price),
      };
    });
});

/*
  Computed que identifica listings com avaliação inferior a 3 estrelas.
  Normaliza ratings que possam estar em escala 0-100 para 0-5.
*/
const lowRatingData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        appliedneighbourhood.value &&
        i.neighbourhood_cleansed !== appliedneighbourhood.value
      )
        return false;
      if (!i.review_scores_rating) return false;
      let r = parseFloat(i.review_scores_rating);
      if (r > 5) r = r / 20;
      return r < 3 && r > 0;
    })
    .map((i) => {
      let rating = parseFloat(i.review_scores_rating);
      if (rating > 5) rating = rating / 20;
      return {
        id: i.id,
        name: i.name,
        sub: i.neighbourhood_cleansed,
        category: "Poor Quality",
        metric: rating.toFixed(1),
        price: formatPrice(i.price),
      };
    });
});

/*
  Computed que identifica listings com menos de 60 dias ocupados (baixa procura).
*/
const lowOccupancyData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        appliedneighbourhood.value &&
        i.neighbourhood_cleansed !== appliedneighbourhood.value
      )
        return false;
      const occupied = 365 - (parseInt(i.availability_365) || 0);
      return occupied < 60;
    })
    .map((i) => ({
      id: i.id,
      name: i.name,
      sub: i.neighbourhood_cleansed,
      category: "Low Demand",
      metric: `${365 - (parseInt(i.availability_365) || 0)} days occupied`,
      price: formatPrice(i.price),
    }));
});

/*
  Computed que identifica listings com preços 4x acima da média (outliers de preço).
  Calcula a média de preços de todos os listings e filtra os que excedem 400%.
*/
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
        appliedneighbourhood.value &&
        i.neighbourhood_cleansed !== appliedneighbourhood.value
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
    .map((i) => ({
      id: i.id,
      name: i.name,
      sub: i.neighbourhood_cleansed,
      category: "Price Spike",
      metric: "+400% vs Avg",
      price: formatPrice(i.price),
    }));
});

/*
  Computed que identifica listings com preço zero ou inválido (erro de dados).
*/
const zeroPriceData = computed(() => {
  return rawListings.value
    .filter((i) => {
      if (
        appliedneighbourhood.value &&
        i.neighbourhood_cleansed !== appliedneighbourhood.value
      )
        return false;
      const p = parseFloat(String(i.price).replace(/[$,]/g, "")) || 0;
      return p === 0;
    })
    .map((i) => ({
      id: i.id,
      name: i.name || "Unknown Listing",
      sub: i.neighbourhood_cleansed,
      category: "Data Error",
      metric: "Invalid Price",
      price: "€0",
    }));
});

// Seleciona os dados da tabela com base no tipo de anomalia ativo
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

const totalPages = computed(() =>
  Math.ceil(currentTableData.value.length / itemsPerPage)
);

const paginatedTableData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return currentTableData.value.slice(start, end);
});

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// Reinicia a página ao mudar de tipo de anomalia
watch(activeAnomaly, () => {
  currentPage.value = 1;
});

// Título legível para a categoria de anomalia selecionada
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

/*
  Exporta os detalhes de uma anomalia específica para PDF.
  Inclui metadados do filtro aplicado e detalhes do item selecionado.
*/
const exportAnomalyRow = (item) => {
  const doc = new jsPDF();

  // Title
  doc.setFontSize(18);
  doc.text(`Anomaly Report - ${item.category}`, 14, 22);

  // Metadata
  doc.setFontSize(10);
  doc.setTextColor(100);
  const cityLabel =
    appliedCity.value.charAt(0).toUpperCase() + appliedCity.value.slice(1);
  const periodLabel =
    store.PERIODS.find((p) => p.value === appliedPeriod.value)?.label ||
    appliedPeriod.value;
  const neighbourhoodLabel = appliedneighbourhood.value || "All Neighbourhoods";
  doc.text(
    `Generated: ${new Date().toLocaleDateString()} | City: ${cityLabel} | Period: ${periodLabel} | Neighbourhood: ${neighbourhoodLabel}`,
    14,
    30
  );

  // Anomaly details
  doc.setFontSize(12);
  doc.setTextColor(0);

  const metricLabel = (() => {
    switch (activeAnomaly.value) {
      case "multiHost":
        return "Listings Count";
      case "highOccupancy":
        return "Days Occupied";
      case "lowRating":
        return "Rating";
      case "lowOccupancy":
        return "Days Occupied";
      case "priceSpike":
        return "Price Variation";
      case "zeroPrice":
        return "Price Status";
      default:
        return "Metric";
    }
  })();

  const details = [
    ["Category", item.category],
    ["ID", String(item.id)],
    [
      activeAnomaly.value === "multiHost" ? "Host Name" : "Listing Name",
      item.name,
    ],
  ];

  if (activeAnomaly.value !== "multiHost") {
    details.push(["Location", item.sub]);
  }

  details.push([metricLabel, item.metric]);

  if (item.price && item.price !== "-") {
    details.push(["Price", item.price]);
  }

  autoTable(doc, {
    body: details,
    startY: 40,
    theme: "plain",
    styles: {
      fontSize: 11,
      cellPadding: 4,
    },
    columnStyles: {
      0: { fontStyle: "bold", cellWidth: 50 },
      1: { cellWidth: 120 },
    },
  });

  doc.save(
    `anomaly_${item.category.toLowerCase().replace(/\s+/g, "_")}_${item.id}.pdf`
  );
};
</script>

<style scoped>
/* LAYOUT */
.anomalies-page {
  width: 100%;
  max-width: 1000px;
  padding: 2rem 1rem;
  color: black;
}

/* HEADER */
.header-section {
  margin-bottom: 2rem;
}

.header-section h1 {
  margin: 0 0 1.5rem 0;
  font-size: 2rem;
  font-weight: 800;
}

/* FILTERS BAR */
.filters-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 16px;
}

.input-group {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  color: grey;
  pointer-events: none;
}

.filters-bar select {
  width: 100%;
  padding: 10px 12px 10px 40px;
  font-size: 0.9rem;
  color: black;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  cursor: pointer;
}

.btn-apply {
  padding: 10px 24px;
  font-weight: 600;
  color: white;
  background-color: #ff5a5f;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-reset {
  padding: 10px 24px;
  font-weight: 600;
  color: #666;
  background-color: #f0f0f0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-reset:hover {
  background-color: #e0e0e0;
}

/* ALERTS GRID */
.alerts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.alert-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 200px;
  padding: 1.5rem;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.02);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.card-header-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.icon-wrapper {
  display: flex;
  color: #ff5a5f;
}

.icon-wrapper svg {
  width: 24px;
  height: 24px;
}

.alert-card h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.3;
  color: #333;
}

.card-description {
  flex-grow: 1;
  margin: 0 0 1.5rem 0;
  font-size: 0.85rem;
  line-height: 1.5;
  color: grey;
}

.btn-view {
  width: 100%;
  padding: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #ff5a5f;
  background-color: #fff0f0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-view:hover {
  background-color: #ffe0e0;
}

/* DETAILS SECTION */
.details-section h2 {
  margin-bottom: 0.5rem;
  font-size: 1.4rem;
  font-weight: 800;
  color: #333;
}

.details-section h2 span {
  color: #ff5a5f;
}

/* TABLE */
.table-card {
  overflow: hidden;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

table {
  width: 100%;
  font-size: 0.9rem;
  border-collapse: collapse;
}

th {
  padding: 16px 24px;
  font-size: 0.7rem;
  font-weight: 700;
  color: #6b7280;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background-color: #f9fafb;
}

td {
  padding: 16px 24px;
  color: #333;
  vertical-align: middle;
  border-bottom: 1px solid #f0f0f0;
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
  padding: 6px 10px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #ff5a5f;
  text-transform: uppercase;
  background: #fff0f0;
  border-radius: 8px;
}

.metric-value {
  font-weight: 600;
  color: #333;
}

.btn-table {
  padding: 6px 14px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #333;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-table:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.btn-export-csv {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #ff5a5f;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-export-csv:hover {
  opacity: 0.7;
}

.btn-export-csv svg {
  flex-shrink: 0;
}

.table-footer-bar {
  height: 20px;
  background: white;
}

/* PAGINATION */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-top: 1px solid #f0f0f0;
}

.pagination-btn {
  padding: 8px 16px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #ff5a5f;
  background: white;
  border: 1px solid #ff5a5f;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #ff5a5f;
  color: white;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.85rem;
  color: #6b7280;
}

/* STATES */
.empty-row,
.loading-state {
  padding: 3rem;
  color: grey;
  font-style: italic;
  text-align: center;
}
</style>
