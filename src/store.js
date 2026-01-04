/* 
  Store reativa global da aplicação InsideView.
  
  Este ficheiro exporta um objeto store que gere o estado partilhado:
  - currency: a moeda selecionada pelo utilizador (EUR, USD, GBP)
  - period: o período temporal selecionado (2025-03, 2025-06, 2025-09)
  
  Os valores são persistidos em sessionStorage para manter o estado entre recarregamentos.
*/
import { reactive, readonly } from "vue";

// Valores iniciais obtidos do sessionStorage ou valores por defeito
const initialCurrency = sessionStorage.getItem("currency") || "EUR";
const initialPeriod = sessionStorage.getItem("period") || "2025-09";

// Períodos disponíveis para seleção na aplicação
const PERIODS = [
  { value: "2025-03", label: "Mar 2025" },
  { value: "2025-06", label: "Jun 2025" },
  { value: "2025-09", label: "Sep 2025" },
];

const state = reactive({
  currency: initialCurrency,
  period: initialPeriod,
});

/*
  Guarda a moeda selecionada no estado e em sessionStorage.
*/
function saveCurrency(newCurrency) {
  state.currency = newCurrency;
  sessionStorage.setItem("currency", newCurrency);
}

/*
  Guarda o período selecionado no estado e em sessionStorage.
*/
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
