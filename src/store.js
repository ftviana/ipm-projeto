import { reactive, readonly } from "vue";

const initialCurrency = sessionStorage.getItem("currency") || "EUR";
const initialPeriod = sessionStorage.getItem("period") || "2025-09";

const PERIODS = [
  { value: "2025-03", label: "Mar 2025" },
  { value: "2025-06", label: "Jun 2025" },
  { value: "2025-09", label: "Sep 2025" },
];

const state = reactive({
  currency: initialCurrency,
  period: initialPeriod,
});

function saveCurrency(newCurrency) {
  state.currency = newCurrency;
  sessionStorage.setItem("currency", newCurrency);
}

function savePeriod(newPeriod) {
  state.period = newPeriod;
  sessionStorage.setItem("period", newPeriod);
}

export const store = {
  state: readonly(state),
  PERIODS,
  saveCurrency,
  savePeriod,
};
