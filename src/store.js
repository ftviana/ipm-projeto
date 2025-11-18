import { reactive, readonly } from 'vue'

const initialCurrency = sessionStorage.getItem('currency') || 'USD'

const state = reactive({
  currency: initialCurrency
})

function saveCurrency(newCurrency) {
  state.currency = newCurrency
  sessionStorage.setItem('currency', newCurrency)
}

export const store = {
  state: readonly(state),
  saveCurrency,
}