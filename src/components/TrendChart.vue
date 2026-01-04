<!-- 
  Componente TrendChart - Gráfico de linha para tendências.
  
  Props:
  - labels: Array de labels para o eixo X
  - values: Array de valores para o eixo Y
  - color: Cor da linha (default: #FF5A5F)
  - label: Legenda do dataset
-->
<template>
  <div class="chart-container">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const props = defineProps({
  labels: Array,
  values: Array,
  color: { type: String, default: "#FF5A5F" },
  label: String,
});

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: props.label,
      backgroundColor: props.color,
      borderColor: props.color,
      data: props.values,
      tension: 0.4,
      pointRadius: 0,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { mode: "index", intersect: false },
  },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 10 } } },
    y: { display: false },
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style>
