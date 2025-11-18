<script setup>
import { ref } from 'vue'
import { store } from '../store.js'
import AppToast from '../components/AppToast.vue'

const localCurrency = ref(store.state.currency)

const showToast = ref(false)

function saveChanges() {

  store.saveCurrency(localCurrency.value)
  
  showToast.value = true
  
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

function resetToDefaults() {
  localCurrency.value = 'USD'
  saveChanges()
}
</script>

<template>

  <div class="settings-page">
    
    <div class="header">
      <h1>Settings</h1>
      <p class="subtitle">Personalize your experience</p>
    </div>

    <section class="settings-section">
      <h2>Preferred Currency</h2>
      <p class="description">Define how you want to see the data presented.</p>
      
      <div class="currency-switcher">
        <button 
          :class="{ active: localCurrency === 'USD' }" 
          @click="localCurrency = 'USD'">
          USD
        </button>
        <button 
          :class="{ active: localCurrency === 'EUR' }" 
          @click="localCurrency = 'EUR'">
          EUR
        </button>
        <button 
          :class="{ active: localCurrency === 'GBP' }" 
          @click="localCurrency = 'GBP'">
          GBP
        </button>
      </div>
    </section>

    <section class="actions-row">
      <button class="btn-save" @click="saveChanges">Save Changes</button>
      <button class="btn-reset" @click="resetToDefaults">Reset to Defaults</button>
    </section>

    <div class="toast-wrapper">
      <Transition name="fade">
        <AppToast v-if="showToast" />
      </Transition>
    </div>

    <p class="footer-note">
      Your preferences are locally saved on this device.
    </p>

  </div>
</template>

<style scoped>

.settings-page {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  padding: 4rem 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2.5rem;
}

.header h1 {
  font-weight: 800; font-size: 2.5rem; margin: 0; color: #111827;
}

.header .subtitle {
  font-size: 1rem; color: #6b7280; margin: 0.25rem 0 0 0;
}

.settings-section {
  width: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 0.75rem;
}

.settings-section h2 {
  font-weight: 700; font-size: 1.2rem; color: #111827; margin: 0;
}

.settings-section .description {
  font-size: 0.9rem; color: #6b7280; margin: 0 0 0.5rem 0;
}

.currency-switcher {
  display: flex; width: 100%; gap: 1rem;
}

.currency-switcher button {
  flex: 1; border: 1px solid #e5e7eb; background-color: #ffffff; color: #111827;
  padding: 1rem; font-size: 1rem; font-weight: 600; border-radius: 16px; cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.currency-switcher button.active {
  background-color: #ED6A6A; color: #ffffff; border-color: #ED6A6A;
}

.actions-row {
  display: flex; width: 100%; gap: 1rem; margin-top: 1rem;
}

.toast-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  position: relative;
  height: 0;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease;
}

.actions-row button {
  flex: 1; padding: 1rem; font-size: 1rem; font-weight: 600; border-radius: 16px;
  cursor: pointer; border: 1px solid transparent; transition: all 0.2s ease;
}

.btn-save {
  background-color: #ED6A6A; color: #ffffff; border-color: #ED6A6A;
}

.btn-save:hover { background-color: #e05a5a; }
.btn-reset {
  background-color: #ffffff; color: #ED6A6A; border-color: #ED6A6A;
}

.btn-reset:hover { background-color: #fefafa; }
.footer-note {
  width: 100%; text-align: center; font-size: 0.8rem; color: #9ca3af; margin-top: 2rem;
}
</style>